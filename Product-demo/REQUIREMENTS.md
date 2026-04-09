# Requirements — Gen-AI Product Manager

## 1. Product Overview

**Product Name:** Gen-AI Product Manager  
**Version:** 1.0.0  
**Author:** Subramonian Attringal  
**License:** MIT  

A multi-agent generative AI system that transforms raw product ideas into complete strategy artifacts and Jira-ready execution plans, eliminating weeks of manual product management work.

---

## 2. Functional Requirements

### 2.1 Core Processing

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-01 | System accepts free-text product ideas (10–5000 characters) via REST API | Critical |
| FR-02 | System routes input to the appropriate specialist agent automatically (intent detection) | Critical |
| FR-03 | User can explicitly select any of the 7 agents, bypassing auto-routing | High |
| FR-04 | System returns structured JSON output for each agent | Critical |
| FR-05 | System returns raw LLM text alongside structured output | Medium |
| FR-06 | All API responses complete within 60 seconds | High |

### 2.2 Specialist Agents

| ID | Agent | Output | Priority |
|----|-------|--------|----------|
| FR-10 | Lean Idea Architect | Lean Canvas (9 fields) | Critical |
| FR-11 | Business Modeler | Business Model Canvas (9 fields) | High |
| FR-12 | Value Proposition Designer | VPC (6 fields) | High |
| FR-13 | Visionary | Vision statement, mission, narrative | High |
| FR-14 | OKR Strategist | 3–4 OKRs with key results + north star metric | High |
| FR-15 | Roadmap Planner | 4-phase roadmap with goals/deliverables | High |
| FR-16 | User Story Teller | Epic + 8–12 Jira-ready user stories | Critical |

### 2.3 Jira Integration

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-20 | System creates Jira Epic from User Story Teller output | High |
| FR-21 | System creates individual Jira Stories under the epic | High |
| FR-22 | Stories include summary, description, priority, and story points | High |
| FR-23 | Acceptance criteria are written in Gherkin format (Given/When/Then) | High |
| FR-24 | Jira push is opt-in per request | Medium |
| FR-25 | System gracefully handles Jira auth failures (returns empty keys list) | High |

### 2.4 Confluence Integration

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-30 | System publishes agent output as a Confluence page | Medium |
| FR-31 | Confluence push is opt-in per request | Medium |
| FR-32 | System returns the published page URL in response | Medium |
| FR-33 | System gracefully handles Confluence auth failures | Medium |

### 2.5 Frontend / User Portal

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-40 | Web portal provides idea input with live character count | Critical |
| FR-41 | Portal displays agent selector with descriptions | High |
| FR-42 | Portal shows loading state during AI processing | High |
| FR-43 | Portal renders user stories in a card-based readable format | High |
| FR-44 | Portal renders all other outputs as formatted JSON | Medium |
| FR-45 | Portal shows Jira issue keys and Confluence URL on completion | Medium |
| FR-46 | Portal provides 3 example ideas to help users get started | Low |
| FR-47 | Dashboard page shows backend health and agent availability | Medium |
| FR-48 | Application is responsive on mobile (360px+) and desktop | High |

---

## 3. Non-Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-01 | Performance | API p95 latency < 60s (LLM-bound) |
| NFR-02 | Availability | 99.5% uptime on Kubernetes (2 replicas) |
| NFR-03 | Security | API keys stored in Kubernetes Secrets, never in code |
| NFR-04 | Security | CORS restricted to configured origins |
| NFR-05 | Security | Container runs as non-root user |
| NFR-06 | Scalability | Backend horizontally scalable via K8s replicas |
| NFR-07 | Observability | Structured JSON logging (structlog) |
| NFR-08 | Maintainability | > 80% test coverage on backend |
| NFR-09 | Portability | Fully containerised; runs on any OCI-compliant runtime |
| NFR-10 | Compatibility | Node.js 20+, Python 3.12+, React 18+ |

---

## 4. External Dependencies

| Dependency | Version | Purpose |
|-----------|---------|---------|
| FastAPI | 0.115.5 | REST API framework |
| LangChain | 0.3.7 | LLM orchestration |
| LangGraph | 0.2.45 | Agentic workflows |
| OpenAI SDK | 1.54.4 | GPT-4o API calls |
| React | 18.3.1 | Frontend UI |
| Vite | 5.4.10 | Frontend build tool |
| Docker | 27+ | Containerisation |
| Kubernetes | 1.29+ | Orchestration |
| Jira REST API | v3 | Issue creation |
| Confluence API | REST | Page publishing |

---

## 5. Constraints

- LLM token limits: Idea input capped at 5000 characters to stay within context window budgets
- LLM provider: Must configure either OpenAI or Azure OpenAI API key before use
- Jira/Confluence: Only user story output triggers Jira push; any output can be published to Confluence
- Rate limits: Subject to OpenAI/Azure rate limits; no client-side queuing in v1.0

---

## 6. Acceptance Criteria

| Scenario | Expected Result |
|----------|----------------|
| User submits an idea with `agent=auto` | Orchestrator detects intent and routes to most appropriate agent |
| User submits an idea with `agent=user_story_teller` and `push_to_jira=true` | Epic + stories created in Jira; issue keys returned in response |
| User submits 9-character idea | 422 Validation Error returned |
| Invalid agent type submitted | 422 Validation Error returned |
| Jira token missing/invalid | Empty `jira_issue_keys` returned; no 500 error |
| Backend container crashes | K8s restarts it; readiness probe prevents traffic until healthy |
