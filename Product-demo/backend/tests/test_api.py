"""
API endpoint tests (FastAPI TestClient).
LLM calls are mocked via respx / monkeypatching.
"""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from main import app
from tests.conftest import SAMPLE_IDEA, MOCK_LEAN_CANVAS, MOCK_USER_STORIES

client = TestClient(app)


# ── Health ────────────────────────────────────────────────────────────────────

class TestHealth:
    def test_health_returns_200(self):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_schema(self):
        data = client.get("/health").json()
        assert "status" in data
        assert "version" in data
        assert "llm_provider" in data
        assert data["status"] == "ok"


# ── Agents list ───────────────────────────────────────────────────────────────

class TestAgentsList:
    def test_agents_returns_200(self):
        resp = client.get("/api/v1/agents")
        assert resp.status_code == 200

    def test_agents_count(self):
        data = client.get("/api/v1/agents").json()
        assert len(data["agents"]) == 7

    def test_agents_have_required_fields(self):
        agents = client.get("/api/v1/agents").json()["agents"]
        for agent in agents:
            assert "id" in agent
            assert "name" in agent
            assert "description" in agent


# ── Process endpoint ──────────────────────────────────────────────────────────

class TestProcessEndpoint:
    def _mock_orchestrator(self, result_agent="lean_idea_architect", output=None):
        from models.schemas import AgentResult, AgentType
        result = AgentResult(
            agent=AgentType(result_agent),
            idea=SAMPLE_IDEA,
            output=output or MOCK_LEAN_CANVAS,
            raw_text=json.dumps(output or MOCK_LEAN_CANVAS),
        )
        return AsyncMock(return_value=result)

    def test_process_requires_idea(self):
        resp = client.post("/api/v1/process", json={})
        assert resp.status_code == 422

    def test_process_idea_too_short(self):
        resp = client.post("/api/v1/process", json={"idea": "hi"})
        assert resp.status_code == 422

    def test_process_lean_canvas(self):
        with patch("main.orchestrator.run", self._mock_orchestrator()):
            resp = client.post("/api/v1/process", json={
                "idea": SAMPLE_IDEA,
                "agent": "lean_idea_architect",
            })
        assert resp.status_code == 200
        data = resp.json()
        assert data["agent"] == "lean_idea_architect"
        assert "output" in data
        assert "problem" in data["output"]

    def test_process_auto_agent(self):
        with patch("main.orchestrator.run", self._mock_orchestrator()):
            resp = client.post("/api/v1/process", json={
                "idea": SAMPLE_IDEA,
                "agent": "auto",
            })
        assert resp.status_code == 200

    def test_process_user_stories_with_jira(self):
        mock = self._mock_orchestrator("user_story_teller", MOCK_USER_STORIES)
        with patch("main.orchestrator.run", mock):
            resp = client.post("/api/v1/process", json={
                "idea": SAMPLE_IDEA,
                "agent": "user_story_teller",
                "push_to_jira": True,
            })
        assert resp.status_code == 200

    def test_invalid_agent_type(self):
        resp = client.post("/api/v1/process", json={
            "idea": SAMPLE_IDEA,
            "agent": "non_existent_agent",
        })
        assert resp.status_code == 422

    def test_process_returns_raw_text(self):
        with patch("main.orchestrator.run", self._mock_orchestrator()):
            resp = client.post("/api/v1/process", json={"idea": SAMPLE_IDEA})
        data = resp.json()
        assert "raw_text" in data
        assert len(data["raw_text"]) > 0
