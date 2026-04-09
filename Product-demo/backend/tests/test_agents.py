"""
Unit tests for each individual agent.
All LLM calls are mocked.
"""
import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from tests.conftest import (
    SAMPLE_IDEA, MOCK_LEAN_CANVAS, MOCK_USER_STORIES
)

MOCK_BMC = {
    "key_partners": ["Cloud providers", "Accounting firms", "Banks"],
    "key_activities": ["Product development", "AI model training", "Customer support"],
    "key_resources": ["Engineering team", "Training data", "Brand"],
    "value_propositions": ["Zero manual entry", "Real-time visibility", "Policy enforcement"],
    "customer_relationships": ["Self-service", "Dedicated CSM", "Community"],
    "channels": ["Direct sales", "Partnerships", "App stores"],
    "customer_segments": ["SMBs", "Enterprises", "Freelancers"],
    "cost_structure": ["Cloud costs", "Staff", "Marketing"],
    "revenue_streams": ["Subscriptions", "Enterprise licenses"],
}

MOCK_VISION = {
    "vision": "A world where finance teams focus on strategy, not paperwork",
    "mission": "Automate expense management with AI so finance teams reclaim their time",
    "strategic_narrative": "Remote work created a receipts chaos...",
    "target_audience": "Finance directors at remote-first companies",
    "differentiators": ["Best-in-class OCR", "Real-time policy enforcement", "Native integrations"],
}

MOCK_OKR = {
    "okrs": [
        {
            "objective": "Become the expense management leader for remote teams",
            "key_results": ["Reach 10,000 active users by Q4 2026", "Achieve NPS > 60"],
            "timeframe": "Q3-Q4 2026",
        }
    ],
    "north_star_metric": "Monthly active users",
}

MOCK_ROADMAP = {
    "phases": [
        {
            "phase": "Phase 1: Foundation",
            "duration": "Months 1-3",
            "goals": ["Launch MVP", "Onboard 100 pilots"],
            "deliverables": ["Receipt scanning", "Approval workflow", "Dashboard"],
            "dependencies": ["OCR service", "Cloud infra"],
        }
    ],
    "total_duration": "12 months",
    "success_criteria": ["1000 paying customers", "< 2 min expense submission"],
}

MOCK_VP = {
    "customer_jobs": ["Submit expenses quickly", "Get reimbursed fast"],
    "pains": ["Manual data entry", "Lost receipts"],
    "gains": ["Faster reimbursement", "Real-time visibility"],
    "pain_relievers": ["OCR auto-fill", "Digital receipt storage"],
    "gain_creators": ["Instant approval workflows", "Live spending dashboards"],
    "products_services": ["Mobile app", "API", "Admin portal"],
}


def make_mock_agent(json_output: dict):
    """Return an agent instance whose LLM returns json_output."""
    mock_llm = AsyncMock()
    mock_llm.ainvoke = AsyncMock(return_value=MagicMock(content=json.dumps(json_output)))
    return mock_llm


@pytest.mark.asyncio
class TestLeanIdeaArchitect:
    async def test_returns_lean_canvas_keys(self):
        from agents.lean_idea_architect import LeanIdeaArchitect
        agent = LeanIdeaArchitect.__new__(LeanIdeaArchitect)
        agent.llm = make_mock_agent(MOCK_LEAN_CANVAS)
        output, raw = await agent.run(SAMPLE_IDEA)
        assert "problem" in output
        assert "unique_value_proposition" in output
        assert isinstance(output["problem"], list)

    async def test_handles_invalid_json_gracefully(self):
        from agents.lean_idea_architect import LeanIdeaArchitect
        mock_llm = AsyncMock()
        mock_llm.ainvoke = AsyncMock(return_value=MagicMock(content="not json at all"))
        agent = LeanIdeaArchitect.__new__(LeanIdeaArchitect)
        agent.llm = mock_llm
        output, raw = await agent.run(SAMPLE_IDEA)
        assert "raw" in output  # graceful fallback


@pytest.mark.asyncio
class TestBusinessModeler:
    async def test_returns_bmc_keys(self):
        from agents.business_modeler import BusinessModeler
        agent = BusinessModeler.__new__(BusinessModeler)
        agent.llm = make_mock_agent(MOCK_BMC)
        output, _ = await agent.run(SAMPLE_IDEA)
        assert "key_partners" in output
        assert "revenue_streams" in output
        assert "value_propositions" in output


@pytest.mark.asyncio
class TestValuePropositionDesigner:
    async def test_returns_vp_keys(self):
        from agents.value_proposition_designer import ValuePropositionDesigner
        agent = ValuePropositionDesigner.__new__(ValuePropositionDesigner)
        agent.llm = make_mock_agent(MOCK_VP)
        output, _ = await agent.run(SAMPLE_IDEA)
        assert "customer_jobs" in output
        assert "pain_relievers" in output
        assert "gain_creators" in output


@pytest.mark.asyncio
class TestVisionary:
    async def test_returns_vision_keys(self):
        from agents.visionary import Visionary
        agent = Visionary.__new__(Visionary)
        agent.llm = make_mock_agent(MOCK_VISION)
        output, _ = await agent.run(SAMPLE_IDEA)
        assert "vision" in output
        assert "mission" in output
        assert isinstance(output["differentiators"], list)


@pytest.mark.asyncio
class TestOKRStrategist:
    async def test_returns_okr_keys(self):
        from agents.okr_strategist import OKRStrategist
        agent = OKRStrategist.__new__(OKRStrategist)
        agent.llm = make_mock_agent(MOCK_OKR)
        output, _ = await agent.run(SAMPLE_IDEA)
        assert "okrs" in output
        assert "north_star_metric" in output
        assert len(output["okrs"]) > 0

    async def test_okr_has_objective_and_key_results(self):
        from agents.okr_strategist import OKRStrategist
        agent = OKRStrategist.__new__(OKRStrategist)
        agent.llm = make_mock_agent(MOCK_OKR)
        output, _ = await agent.run(SAMPLE_IDEA)
        okr = output["okrs"][0]
        assert "objective" in okr
        assert "key_results" in okr
        assert "timeframe" in okr


@pytest.mark.asyncio
class TestRoadmapPlanner:
    async def test_returns_phases(self):
        from agents.roadmap_planner import RoadmapPlanner
        agent = RoadmapPlanner.__new__(RoadmapPlanner)
        agent.llm = make_mock_agent(MOCK_ROADMAP)
        output, _ = await agent.run(SAMPLE_IDEA)
        assert "phases" in output
        assert len(output["phases"]) > 0
        assert "total_duration" in output

    async def test_phase_has_required_fields(self):
        from agents.roadmap_planner import RoadmapPlanner
        agent = RoadmapPlanner.__new__(RoadmapPlanner)
        agent.llm = make_mock_agent(MOCK_ROADMAP)
        output, _ = await agent.run(SAMPLE_IDEA)
        phase = output["phases"][0]
        for field in ["phase", "duration", "goals", "deliverables", "dependencies"]:
            assert field in phase


@pytest.mark.asyncio
class TestUserStoryTeller:
    async def test_returns_epic_and_stories(self):
        from agents.user_story_teller import UserStoryTeller
        agent = UserStoryTeller.__new__(UserStoryTeller)
        agent.llm = make_mock_agent(MOCK_USER_STORIES)
        output, _ = await agent.run(SAMPLE_IDEA)
        assert "epic_name" in output
        assert "stories" in output
        assert len(output["stories"]) > 0

    async def test_story_has_acceptance_criteria(self):
        from agents.user_story_teller import UserStoryTeller
        agent = UserStoryTeller.__new__(UserStoryTeller)
        agent.llm = make_mock_agent(MOCK_USER_STORIES)
        output, _ = await agent.run(SAMPLE_IDEA)
        story = output["stories"][0]
        assert "acceptance_criteria" in story
        ac = story["acceptance_criteria"][0]
        assert "given" in ac and "when" in ac and "then" in ac

    async def test_story_points_are_fibonacci(self):
        from agents.user_story_teller import UserStoryTeller
        agent = UserStoryTeller.__new__(UserStoryTeller)
        agent.llm = make_mock_agent(MOCK_USER_STORIES)
        output, _ = await agent.run(SAMPLE_IDEA)
        valid_points = {1, 2, 3, 5, 8, 13, 21}
        for s in output["stories"]:
            assert s["story_points"] in valid_points
