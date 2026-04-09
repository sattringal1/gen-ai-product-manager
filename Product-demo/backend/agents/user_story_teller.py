import json
from langchain_core.messages import HumanMessage, SystemMessage
from agents.base import BaseAgent
from models.schemas import UserStorySet

SYSTEM_PROMPT = """You are a Senior Agile Coach and BA. Given a product idea, generate a full epic with Jira-ready user stories.
Return ONLY valid JSON:
{
  "epic_name": "string",
  "epic_summary": "string",
  "stories": [
    {
      "title": "string",
      "as_a": "string (persona)",
      "i_want": "string (action)",
      "so_that": "string (benefit)",
      "acceptance_criteria": [
        {"given": "string", "when": "string", "then": "string"}
      ],
      "story_points": integer (1,2,3,5,8,13),
      "priority": "Critical|High|Medium|Low",
      "labels": ["string", ...],
      "epic": "string (epic name)"
    }
  ]
}
Generate 8-12 user stories covering core flows. Each story needs 2-3 acceptance criteria in Gherkin format."""


class UserStoryTeller(BaseAgent):
    name = "user_story_teller"

    async def run(self, idea: str) -> tuple[dict, str]:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Product idea: {idea}"),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content
        try:
            data = json.loads(raw)
            stories = UserStorySet(**data)
            return stories.model_dump(), raw
        except Exception:
            return {"raw": raw}, raw
