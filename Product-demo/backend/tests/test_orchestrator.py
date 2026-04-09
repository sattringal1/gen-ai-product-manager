"""
Tests for the Orchestrator intent-routing and agent dispatch logic.
"""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from models.schemas import ProcessRequest, AgentType
from tests.conftest import SAMPLE_IDEA, MOCK_LEAN_CANVAS, MOCK_USER_STORIES


def make_llm(response_text: str):
    mock = AsyncMock()
    mock.ainvoke = AsyncMock(return_value=MagicMock(content=response_text))
    return mock


@pytest.mark.asyncio
class TestOrchestrator:
    async def _get_orchestrator(self, intent_response="lean_idea_architect", agent_output=None):
        from agents.orchestrator import Orchestrator
        orch = Orchestrator.__new__(Orchestrator)
        orch.llm = make_llm(intent_response)
        orch.jira = MagicMock()
        orch.jira.create_stories = AsyncMock(return_value=["PM-1", "PM-2"])
        orch.confluence = MagicMock()
        orch.confluence.publish_page = AsyncMock(return_value="https://confluence.example.com/page/1")
        # Patch the agent to avoid real LLM calls
        if agent_output:
            mock_agent = AsyncMock()
            mock_agent.run = AsyncMock(return_value=(agent_output, json.dumps(agent_output)))
            with patch("agents.orchestrator.AGENT_MAP", {AgentType.LEAN_IDEA_ARCHITECT: lambda: mock_agent}):
                pass
        return orch

    async def test_auto_routes_to_detected_agent(self):
        from agents.orchestrator import Orchestrator
        orch = await self._get_orchestrator()
        # Patch intent detection
        orch.llm = make_llm("lean_idea_architect")
        # Patch agent
        mock_agent = MagicMock()
        mock_agent.run = AsyncMock(return_value=(MOCK_LEAN_CANVAS, json.dumps(MOCK_LEAN_CANVAS)))
        with patch.dict("agents.orchestrator.AGENT_MAP", {AgentType.LEAN_IDEA_ARCHITECT: lambda: mock_agent}):
            req = ProcessRequest(idea=SAMPLE_IDEA, agent=AgentType.AUTO)
            result = await orch.run(req)
        assert result.agent == AgentType.LEAN_IDEA_ARCHITECT

    async def test_explicit_agent_skips_intent_detection(self):
        from agents.orchestrator import Orchestrator
        orch = await self._get_orchestrator()
        mock_agent = MagicMock()
        mock_agent.run = AsyncMock(return_value=(MOCK_USER_STORIES, json.dumps(MOCK_USER_STORIES)))
        with patch.dict("agents.orchestrator.AGENT_MAP", {AgentType.USER_STORY_TELLER: lambda: mock_agent}):
            req = ProcessRequest(idea=SAMPLE_IDEA, agent=AgentType.USER_STORY_TELLER)
            result = await orch.run(req)
        assert result.agent == AgentType.USER_STORY_TELLER
        # LLM intent detection should NOT have been called
        orch.llm.ainvoke.assert_not_called()

    async def test_push_to_jira_calls_jira_client(self):
        from agents.orchestrator import Orchestrator
        orch = await self._get_orchestrator()
        mock_agent = MagicMock()
        mock_agent.run = AsyncMock(return_value=(MOCK_USER_STORIES, json.dumps(MOCK_USER_STORIES)))
        with patch.dict("agents.orchestrator.AGENT_MAP", {AgentType.USER_STORY_TELLER: lambda: mock_agent}):
            req = ProcessRequest(idea=SAMPLE_IDEA, agent=AgentType.USER_STORY_TELLER, push_to_jira=True)
            result = await orch.run(req)
        orch.jira.create_stories.assert_called_once()
        assert result.jira_issue_keys == ["PM-1", "PM-2"]

    async def test_push_to_confluence_calls_confluence_client(self):
        from agents.orchestrator import Orchestrator
        orch = await self._get_orchestrator()
        mock_agent = MagicMock()
        mock_agent.run = AsyncMock(return_value=(MOCK_LEAN_CANVAS, json.dumps(MOCK_LEAN_CANVAS)))
        with patch.dict("agents.orchestrator.AGENT_MAP", {AgentType.LEAN_IDEA_ARCHITECT: lambda: mock_agent}):
            req = ProcessRequest(idea=SAMPLE_IDEA, agent=AgentType.LEAN_IDEA_ARCHITECT, push_to_confluence=True)
            result = await orch.run(req)
        orch.confluence.publish_page.assert_called_once()
        assert result.confluence_page_url is not None

    async def test_invalid_intent_falls_back_to_lean_canvas(self):
        from agents.orchestrator import Orchestrator
        orch = await self._get_orchestrator("garbage_response")
        detected = await orch._detect_intent("some random idea")
        assert detected == AgentType.LEAN_IDEA_ARCHITECT
