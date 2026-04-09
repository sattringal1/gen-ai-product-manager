"""
Intent-aware orchestrator — routes a product idea to the right agent
or runs ALL agents in sequence when agent=AUTO.
"""
import asyncio
import structlog
from langchain_core.messages import HumanMessage, SystemMessage

from agents.base import get_llm
from agents.lean_idea_architect import LeanIdeaArchitect
from agents.business_modeler import BusinessModeler
from agents.value_proposition_designer import ValuePropositionDesigner
from agents.visionary import Visionary
from agents.okr_strategist import OKRStrategist
from agents.roadmap_planner import RoadmapPlanner
from agents.user_story_teller import UserStoryTeller
from models.schemas import ProcessRequest, AgentResult, AgentType
from integrations.jira_client import JiraClient
from integrations.confluence_client import ConfluenceClient

log = structlog.get_logger()

AGENT_MAP = {
    AgentType.LEAN_IDEA_ARCHITECT: LeanIdeaArchitect,
    AgentType.BUSINESS_MODELER: BusinessModeler,
    AgentType.VALUE_PROPOSITION_DESIGNER: ValuePropositionDesigner,
    AgentType.VISIONARY: Visionary,
    AgentType.OKR_STRATEGIST: OKRStrategist,
    AgentType.ROADMAP_PLANNER: RoadmapPlanner,
    AgentType.USER_STORY_TELLER: UserStoryTeller,
}

INTENT_SYSTEM_PROMPT = """You are a product management routing agent.
Given a product idea, choose the single best agent to use first.
Reply with ONLY one of these agent IDs (no explanation):
lean_idea_architect | business_modeler | value_proposition_designer |
visionary | okr_strategist | roadmap_planner | user_story_teller

Choose based on:
- "idea/concept/problem" → lean_idea_architect
- "business model/revenue/partners" → business_modeler
- "customer pain/value/need" → value_proposition_designer
- "vision/mission/strategy" → visionary
- "goals/objectives/OKR" → okr_strategist
- "roadmap/plan/timeline/phases" → roadmap_planner
- "stories/features/sprint/jira" → user_story_teller
"""


class Orchestrator:
    def __init__(self):
        self.llm = get_llm()
        self.jira = JiraClient()
        self.confluence = ConfluenceClient()

    async def _detect_intent(self, idea: str) -> AgentType:
        messages = [
            SystemMessage(content=INTENT_SYSTEM_PROMPT),
            HumanMessage(content=idea),
        ]
        response = await self.llm.ainvoke(messages)
        agent_id = response.content.strip().lower()
        try:
            return AgentType(agent_id)
        except ValueError:
            log.warning("intent_detection_fallback", raw=agent_id)
            return AgentType.LEAN_IDEA_ARCHITECT

    async def run(self, req: ProcessRequest) -> AgentResult:
        agent_type = req.agent
        if agent_type == AgentType.AUTO:
            agent_type = await self._detect_intent(req.idea)
            log.info("intent_detected", agent=agent_type)

        agent_cls = AGENT_MAP[agent_type]
        agent = agent_cls()
        output, raw_text = await agent.run(req.idea)

        jira_keys: list[str] = []
        confluence_url: str | None = None

        # Push user stories to Jira if requested
        if req.push_to_jira and agent_type == AgentType.USER_STORY_TELLER:
            project_key = req.jira_project_key or None
            jira_keys = await self.jira.create_stories(output, project_key)

        # Publish to Confluence if requested
        if req.push_to_confluence:
            space_key = req.confluence_space_key or None
            confluence_url = await self.confluence.publish_page(
                title=f"AI Output: {req.idea[:60]}",
                body=raw_text,
                space_key=space_key,
            )

        return AgentResult(
            agent=agent_type,
            idea=req.idea,
            output=output,
            raw_text=raw_text,
            jira_issue_keys=jira_keys,
            confluence_page_url=confluence_url,
        )
