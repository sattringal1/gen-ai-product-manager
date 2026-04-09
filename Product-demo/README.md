# Gen-AI Product Manager

> From raw product idea → vision → roadmap → Jira-ready execution — powered by Agentic AI.

A multi-agent AI system built with **FastAPI**, **LangChain**, **LangGraph**, and **React** that transforms product ideas into complete strategy artifacts in seconds.

**Author:** Subramonian Attringal | [GitHub](https://github.com/sattringal1) | [LinkedIn](https://www.linkedin.com/in/subramonian-attringal/)

---

## Quick Start

```bash
# 1. Clone and configure
git clone https://github.com/sattringal1/gen-ai-product-manager
cd gen-ai-product-manager/Product-demo
cp .env.example .env
# Edit .env — set OPENAI_API_KEY at minimum

# 2. Run with Docker Compose
docker-compose up --build -d

# 3. Open the portal
open http://localhost:3000/portal
```

---

## Architecture

```
User → React Portal → FastAPI Backend → Orchestrator (GPT-4o intent router)
                                               ↓
                           ┌──────────────────────────────────┐
                           │         7 Specialist Agents       │
                           │  Lean Canvas  | Business Model    │
                           │  Value Prop   | Vision & Mission  │
                           │  OKRs         | Roadmap           │
                           │  User Stories                     │
                           └──────────────────────────────────┘
                                               ↓
                               Jira API ←──────────→ Confluence API
```

---

## 7 AI Agents

| Agent | Output |
|-------|--------|
| Lean Idea Architect | Lean Canvas — Problem, Solution, UVP, Channels, Key Metrics |
| Business Modeler | Business Model Canvas (all 9 blocks) |
| Value Proposition Designer | Customer Profile + Value Map |
| Visionary | Vision statement, mission, strategic pillars |
| OKR Strategist | Objectives + measurable Key Results |
| Roadmap Planner | 4-phase phased roadmap with milestones |
| User Story Teller | Epic + Jira-ready user stories with acceptance criteria |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend API | Python 3.12, FastAPI, Uvicorn |
| AI / LLM | LangChain 0.3, LangGraph 0.2, OpenAI GPT-4o |
| Frontend | React 18, Vite 5, React Router 6 |
| Infrastructure | Docker Compose, Kubernetes (AKS-ready) |
| Integrations | Jira REST API v3, Confluence REST API |
| Auth | python-jose, passlib (bcrypt) |
| Testing | pytest, pytest-asyncio, Vitest |

---

## Project Structure

```
Product-demo/
├── backend/
│   ├── main.py                        # FastAPI entry point + API routes
│   ├── config.py                      # Pydantic settings (env-driven)
│   ├── agents/
│   │   ├── orchestrator.py            # LLM-based intent router
│   │   ├── base.py                    # Shared agent base class
│   │   ├── lean_idea_architect.py
│   │   ├── business_modeler.py
│   │   ├── value_proposition_designer.py
│   │   ├── visionary.py
│   │   ├── okr_strategist.py
│   │   ├── roadmap_planner.py
│   │   └── user_story_teller.py
│   ├── models/
│   │   └── schemas.py                 # Pydantic request/response models
│   ├── integrations/
│   │   ├── jira_client.py             # Jira Epic + Story creation
│   │   └── confluence_client.py       # Confluence page publishing
│   ├── tests/                         # pytest test suites
│   ├── requirements.txt
│   ├── pytest.ini
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Portal.jsx             # Main multi-agent portal
│   │   │   ├── Portal.css
│   │   │   ├── Home.jsx               # Landing page
│   │   │   └── Dashboard.jsx          # Analytics dashboard
│   │   ├── components/
│   │   │   ├── AgentSelector.jsx      # Multi-select checkbox agent picker
│   │   │   ├── AgentSelector.css
│   │   │   ├── ResultsDashboard.jsx   # Live results grid + export
│   │   │   ├── ResultsDashboard.css
│   │   │   └── Navigation.jsx
│   │   ├── api/
│   │   │   └── client.js              # Axios API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css                  # Global design tokens
│   ├── index.html
│   ├── vite.config.js
│   ├── package.json
│   ├── nginx.conf
│   └── Dockerfile
│
├── k8s/                               # Kubernetes manifests (AKS-ready)
│   ├── namespace.yaml
│   ├── configmap.yaml
│   ├── backend-deployment.yaml
│   ├── frontend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-service.yaml
│   └── ingress.yaml
│
├── docker-compose.yml
├── .env.example                       # Template — copy to .env
├── .gitignore
├── REQUIREMENTS.md
├── TEST_PLAN.md
├── DEPLOYMENT.md
└── USER_PORTAL_GUIDE.md
```

---

## Key Features

- **Multi-agent parallel execution** — select any combination of the 7 agents; they run in parallel and results appear live
- **Results Dashboard** — polished card grid with structured output per agent
- **Export to PDF** — one-click full dashboard capture
- **Export to PowerPoint** — auto-generated `.pptx` with title slide + one slide per agent
- **Jira integration** — push user stories as Epic + sub-tasks directly from the portal
- **Confluence integration** — publish any output as a Confluence page
- **Docker Compose** — single command local deployment
- **Kubernetes ready** — AKS manifests included for production deployment

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `OPENAI_MODEL` | No | Default: `gpt-4o` |
| `LLM_PROVIDER` | No | `openai` or `azure_openai` |
| `JIRA_BASE_URL` | Optional | e.g. `https://myorg.atlassian.net` |
| `JIRA_API_TOKEN` | Optional | Jira personal access token |
| `CONFLUENCE_BASE_URL` | Optional | Confluence base URL |
| `CONFLUENCE_API_TOKEN` | Optional | Confluence personal access token |

See `.env.example` for the full list.

---

## Documentation

| File | Description |
|------|-------------|
| [REQUIREMENTS.md](REQUIREMENTS.md) | Functional + non-functional requirements |
| [TEST_PLAN.md](TEST_PLAN.md) | Full test plan and running instructions |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Local, Docker, and Kubernetes deployment guide |
| [USER_PORTAL_GUIDE.md](USER_PORTAL_GUIDE.md) | End-user portal guide + API reference |

---

## License

MIT © 2026 Subramonian Attringal
