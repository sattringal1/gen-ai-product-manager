"""
Shared fixtures for all backend tests.
LLM calls are mocked by default — set INTEGRATION_TESTS=true to call real APIs.
"""
import os
import json
import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from httpx import AsyncClient
from fastapi.testclient import TestClient

# Keep settings deterministic during tests
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("LLM_PROVIDER", "openai")

from main import app

# ── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
def test_client():
    return TestClient(app)


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


SAMPLE_IDEA = "An AI-powered expense management app for remote-first companies"

MOCK_LEAN_CANVAS = {
    "problem": ["Manual expense reporting is slow", "Lost receipts waste time", "No real-time visibility"],
    "customer_segments": ["Remote-first companies", "Finance teams", "Employees who travel"],
    "unique_value_proposition": "AI-automated expense management with zero manual data entry",
    "solution": ["OCR receipt scanning", "AI categorisation", "Real-time dashboards"],
    "channels": ["Direct sales", "Partner ecosystem", "App marketplaces"],
    "revenue_streams": ["Monthly SaaS subscription", "Enterprise licensing", "API access"],
    "cost_structure": ["Cloud infrastructure", "ML model training", "Sales & marketing"],
    "key_metrics": ["Monthly active users", "Receipts processed/day", "Time-to-reimbursement"],
    "unfair_advantage": "Proprietary receipt OCR trained on 10M expense documents",
}

MOCK_USER_STORIES = {
    "epic_name": "Expense Submission",
    "epic_summary": "Enable employees to submit expenses via mobile",
    "stories": [
        {
            "title": "Upload receipt photo",
            "as_a": "remote employee",
            "i_want": "to photograph my receipt and have it auto-filled",
            "so_that": "I never type expense details manually",
            "acceptance_criteria": [
                {"given": "I am on the submit screen", "when": "I tap 'Scan Receipt'", "then": "Camera opens"},
                {"given": "A receipt is photographed", "when": "AI processes it", "then": "Amount and vendor are populated"},
            ],
            "story_points": 5,
            "priority": "High",
            "labels": ["mobile", "ocr"],
            "epic": "Expense Submission",
        }
    ],
}


@pytest.fixture
def mock_llm_lean_canvas():
    """Patches ChatOpenAI.ainvoke to return a Lean Canvas."""
    mock = AsyncMock()
    mock.return_value = MagicMock(content=json.dumps(MOCK_LEAN_CANVAS))
    with patch("agents.base.ChatOpenAI") as mock_cls:
        mock_cls.return_value = mock
        # Also patch the instance method
        with patch("agents.lean_idea_architect.LeanIdeaArchitect.__init__", lambda self: setattr(self, 'llm', mock) or None):
            yield mock


@pytest.fixture
def mock_llm_user_stories():
    mock = AsyncMock()
    mock.return_value = MagicMock(content=json.dumps(MOCK_USER_STORIES))
    return mock
