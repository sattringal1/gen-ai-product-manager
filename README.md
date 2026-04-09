# Gen-AI Product Manager

> From raw product idea → vision → roadmap → Jira-ready execution — powered by Agentic AI.

**Author:** Subramonian Attringal | [GitHub](https://github.com/sattringal1) | [LinkedIn](https://www.linkedin.com/in/subramonian-attringal/)

---

## 🚀 Live Demo

| | Link |
|---|---|
| **Live App** | [https://genai-pm-frontend.blackpond-cceed3d9.westus2.azurecontainerapps.io/portal](https://genai-pm-frontend.blackpond-cceed3d9.westus2.azurecontainerapps.io/portal) |
| **Landing Page** | [https://sattringal1.github.io/gen-ai-product-manager/](https://sattringal1.github.io/gen-ai-product-manager/) |
| **API Docs** | [https://genai-pm-frontend.blackpond-cceed3d9.westus2.azurecontainerapps.io/docs](https://genai-pm-frontend.blackpond-cceed3d9.westus2.azurecontainerapps.io/docs) |

---

## About This Project

This project was built to explore how **Agentic AI** can accelerate the early stages of product management — the messy, time-consuming work of structuring ideas into strategy.

As a Senior PM/TPM, I found that the hardest part of a new initiative is rarely execution — it is clarity. Getting from a raw idea to a shared understanding of the problem, the user, the business model, and the roadmap takes days of workshops and documents. This tool compresses that into seconds.

**What it does:** You describe a product idea in plain language. Seven specialist AI agents run simultaneously, each taking a different strategic lens — Lean Canvas, Business Model Canvas, OKRs, Roadmap, User Stories, and more. Results appear live on a dashboard as each agent completes. You can export the full output to PDF or PowerPoint, or push user stories directly into Jira.

**Why it matters:** It is not a replacement for product thinking — it is a forcing function. The output gives a team something concrete to react to, debate, and refine. The best product conversations start with a draft, not a blank page.

**Built with:** FastAPI + LangChain + LangGraph on the backend, React 18 on the frontend, deployed on Azure Container Apps with GitHub Actions CI/CD.

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
                                               |
                           ┌──────────────────────────────────┐
                           │         7 Specialist Agents       │
                           │  Lean Canvas  | Business Model    │
                           │  Value Prop   | Vision & Mission  │
                           │  OKRs         | Roadmap           │
                           │  User Stories                     │
                           └──────────────────────────────────┘
                                               |
                               Jira API <-----------> Confluence API
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
| Cloud | Azure Container Apps, Azure Container Registry |
| CI/CD | GitHub Actions |
| Integrations | Jira REST API v3, Confluence REST API |
| Testing | pytest, pytest-asyncio, Vitest |

---

## Key Features

- **Multi-agent parallel execution** — select any combination of 7 agents; results appear live as each completes
- **Results Dashboard** — polished card grid with structured output per agent, colour-coded by agent type
- **Export to PDF** — one-click full dashboard capture
- **Export to PowerPoint** — auto-generated `.pptx` with title slide and one slide per agent
- **Jira integration** — push user stories as Epic + sub-tasks directly from the portal
- **Confluence integration** — publish any output as a Confluence page
- **Docker Compose** — single command local deployment
- **Kubernetes ready** — AKS manifests included for production deployment

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
│   ├── models/schemas.py
│   ├── integrations/
│   │   ├── jira_client.py
│   │   └── confluence_client.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/                     # Portal, Home, Dashboard
│   │   ├── components/                # AgentSelector, ResultsDashboard
│   │   └── api/client.js
│   ├── package.json
│   └── Dockerfile
├── k8s/                               # Kubernetes manifests (AKS-ready)
├── docker-compose.yml
├── .env.example
└── *.md docs
```

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
