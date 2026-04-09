# Test Plan — Gen-AI Product Manager

## 1. Testing Strategy

| Layer | Tool | Coverage Target |
|-------|------|----------------|
| Backend unit (agents) | pytest + unittest.mock | > 85% |
| Backend API | FastAPI TestClient | All endpoints |
| Backend integrations | pytest + respx (HTTP mocks) | Jira + Confluence clients |
| Backend orchestrator | pytest-asyncio | Routing + dispatch logic |
| Frontend unit | Vitest + React Testing Library | All components |
| End-to-end (manual) | Browser | Happy path + error paths |

---

## 2. Test Suites

### 2.1 Backend — `backend/tests/`

#### `test_api.py` — HTTP Layer Tests
| Test | Method | Expected |
|------|--------|----------|
| `test_health_returns_200` | GET /health | 200 OK |
| `test_health_schema` | GET /health | status, version, llm_provider keys |
| `test_agents_returns_200` | GET /api/v1/agents | 200 OK |
| `test_agents_count` | GET /api/v1/agents | 7 agents |
| `test_agents_have_required_fields` | GET /api/v1/agents | id, name, description |
| `test_process_requires_idea` | POST /api/v1/process `{}` | 422 |
| `test_process_idea_too_short` | POST with idea="hi" | 422 |
| `test_process_lean_canvas` | POST with agent=lean_idea_architect | 200, output.problem present |
| `test_process_auto_agent` | POST with agent=auto | 200 |
| `test_process_user_stories_with_jira` | POST with push_to_jira=true | 200 |
| `test_invalid_agent_type` | POST with agent=bad_agent | 422 |
| `test_process_returns_raw_text` | POST any agent | raw_text in response |

#### `test_agents.py` — Agent Unit Tests
| Test Class | Tests |
|------------|-------|
| `TestLeanIdeaArchitect` | Returns all 9 Lean Canvas fields; handles invalid JSON gracefully |
| `TestBusinessModeler` | Returns all 9 BMC fields |
| `TestValuePropositionDesigner` | Returns all 6 VP fields |
| `TestVisionary` | Returns vision, mission, differentiators |
| `TestOKRStrategist` | Returns okrs list + north_star_metric; OKR has objective + key_results + timeframe |
| `TestRoadmapPlanner` | Returns phases list; each phase has 5 required fields |
| `TestUserStoryTeller` | Returns epic_name + stories; stories have acceptance_criteria in Gherkin; story_points are Fibonacci |

#### `test_orchestrator.py` — Routing Tests
| Test | Description |
|------|-------------|
| `test_auto_routes_to_detected_agent` | AUTO intent detection routes correctly |
| `test_explicit_agent_skips_intent_detection` | Explicit agent bypasses LLM intent call |
| `test_push_to_jira_calls_jira_client` | `push_to_jira=True` triggers Jira client |
| `test_push_to_confluence_calls_confluence_client` | `push_to_confluence=True` triggers Confluence client |
| `test_invalid_intent_falls_back_to_lean_canvas` | Unknown intent defaults to lean_idea_architect |

#### `test_integrations.py` — Jira & Confluence
| Test | Description |
|------|-------------|
| `test_disabled_when_no_token` (Jira) | Client disabled when no API token |
| `test_enabled_when_credentials_present` | Client enabled with valid config |
| `test_create_epic_returns_key` | Epic creation returns issue key |
| `test_create_story_returns_key` | Story creation returns issue key |
| `test_create_stories_returns_all_keys` | All stories created, all keys returned |
| `test_handles_jira_http_error_gracefully` | 401 returns empty list, no exception |
| `test_disabled_when_no_token` (Confluence) | Client disabled when no token |
| `test_publish_page_returns_url` | Page created, URL returned |
| `test_returns_none_on_error` | 403 returns None, no exception |

### 2.2 Frontend — `frontend/src/test/`

#### `Portal.test.jsx`
| Test | Description |
|------|-------------|
| Renders idea textarea | Textarea with correct placeholder present |
| Disables submit when empty | Submit button disabled with empty idea |
| Enables submit when filled | Button enabled after typing |
| Calls processIdea on submit | API client called with idea payload |
| Shows error on API failure | Error banner displayed |
| Fills idea from example chip | Clicking chip populates textarea |

#### `AgentSelector.test.jsx`
| Test | Description |
|------|-------------|
| Renders all 8 options | All agent cards rendered |
| Highlights selected agent | Selected card has `.selected` class |
| Calls onChange on click | onChange called with agent ID |

---

## 3. Running Tests

### Backend
```bash
cd backend

# Install deps (first time)
pip install -r requirements.txt

# Run all tests
pytest

# Run with coverage report
pytest --cov=. --cov-report=html

# Run specific file
pytest tests/test_agents.py -v

# Run specific test class
pytest tests/test_agents.py::TestUserStoryTeller -v
```

### Frontend
```bash
cd frontend

# Install deps (first time)
npm install

# Run all tests
npm test

# Run in watch mode
npm run test:watch
```

---

## 4. Test Environment Setup

```bash
# Backend test environment variables (auto-set in conftest.py for mocked tests)
export OPENAI_API_KEY=test-key
export LLM_PROVIDER=openai

# To run integration tests against real APIs (optional)
export INTEGRATION_TESTS=true
export OPENAI_API_KEY=sk-real-key
export JIRA_BASE_URL=https://your-org.atlassian.net
export JIRA_API_TOKEN=your-token
export JIRA_EMAIL=you@company.com
```

---

## 5. CI/CD Integration

```yaml
# Example GitHub Actions step
- name: Run backend tests
  working-directory: ./backend
  run: |
    pip install -r requirements.txt
    pytest --tb=short --cov=. --cov-fail-under=80

- name: Run frontend tests
  working-directory: ./frontend
  run: |
    npm ci
    npm test
```
