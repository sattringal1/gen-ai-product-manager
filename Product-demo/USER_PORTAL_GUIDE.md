# End-User Portal Guide — Gen-AI Product Manager

## Getting Started

**Access the portal at:** `http://localhost:3000/portal` (local) or your deployed domain.

---

## The Portal Page

### Step 1 — Enter Your Product Idea

Type a clear description of your product idea in the text area. More detail = better output.

**Good example:**
> "A mobile-first app that helps remote teams track individual wellbeing and prevent burnout using AI-powered check-ins, sentiment analysis, and manager alerts."

**Too vague:**
> "An app"

You can also click one of the **example chips** below the textarea to prefill a sample idea.

---

### Step 2 — Select an Agent

Choose which AI specialist to engage:

| Agent | Best When... | Output |
|-------|-------------|--------|
| **Auto (AI decides)** | You're not sure which to use | Orchestrator picks the best agent |
| **Lean Idea Architect** | You have a raw idea to validate | Lean Canvas (Problem, UVP, Solution, Channels, etc.) |
| **Business Modeler** | You need a business model | Business Model Canvas (9 building blocks) |
| **Value Proposition** | You need to understand customer needs | Pain/gain mapping, products & services |
| **Visionary** | You need a mission/vision | Vision statement, mission, strategic narrative |
| **OKR Strategist** | You need measurable goals | 3–4 OKRs with key results + north star metric |
| **Roadmap Planner** | You need a project plan | 4-phase roadmap with deliverables |
| **User Story Teller** | You need to plan a sprint | Epic + 8–12 Jira-ready stories with Gherkin AC |

---

### Step 3 — Integration Options (Optional)

Click **Integration Options** to expand:

- **Push to Jira** — Available when User Story Teller is selected. Creates an Epic and all stories directly in your Jira project. Requires `JIRA_*` environment variables to be configured.
- **Publish to Confluence** — Publishes the AI output as a page in your Confluence space. Requires `CONFLUENCE_*` environment variables.

---

### Step 4 — Generate

Click **Generate**. Processing typically takes 10–30 seconds depending on the agent and LLM provider.

---

## Reading the Output

### User Story Teller Output (Card View)

Stories are displayed as cards showing:
- **Priority badge** (Critical / High / Medium / Low)
- **Story points**
- **User story** in "As a... I want... so that..." format
- **Acceptance Criteria** in Gherkin (Given / When / Then)
- **Labels** (feature tags)

If Jira push was enabled, the Jira issue keys (e.g., `PM-1, PM-2, PM-3`) appear at the top.

### All Other Agents (JSON View)

Output is shown as formatted JSON. You can copy it to use in your documentation, presentations, or planning tools.

---

## The Dashboard Page

Navigate to `/dashboard` to see:
- **Backend Health** — confirms the API is running and which LLM provider is active
- **Available Agents** — all 7 agents listed with their status
- **Integration Checklist** — which environment variables need to be configured

---

## Quick Reference — API (for Developers)

The backend exposes a full REST API. Interactive docs at `http://localhost:8000/docs`.

### Process an idea (cURL)
```bash
curl -X POST http://localhost:8000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "An AI expense management platform for remote companies",
    "agent": "auto"
  }'
```

### List all agents
```bash
curl http://localhost:8000/api/v1/agents
```

### Check system health
```bash
curl http://localhost:8000/health
```

### Push to Jira
```bash
curl -X POST http://localhost:8000/api/v1/process \
  -H "Content-Type: application/json" \
  -d '{
    "idea": "An AI expense app",
    "agent": "user_story_teller",
    "push_to_jira": true,
    "jira_project_key": "MYPROJECT"
  }'
```

---

## Supported Agent IDs (for API)

| Display Name | API Value |
|-------------|-----------|
| Auto | `auto` |
| Lean Idea Architect | `lean_idea_architect` |
| Business Modeler | `business_modeler` |
| Value Proposition Designer | `value_proposition_designer` |
| Visionary | `visionary` |
| OKR Strategist | `okr_strategist` |
| Roadmap Planner | `roadmap_planner` |
| User Story Teller | `user_story_teller` |

---

## FAQ

**Q: How long does processing take?**  
A: 10–30 seconds typically. Complex roadmap/OKR outputs may take up to 45 seconds.

**Q: My Jira push returned empty keys — what happened?**  
A: Check that `JIRA_BASE_URL`, `JIRA_EMAIL`, `JIRA_API_TOKEN`, and `JIRA_PROJECT_KEY` are set in your `.env` file.

**Q: Can I use Azure OpenAI instead of OpenAI?**  
A: Yes. Set `LLM_PROVIDER=azure_openai` and configure the `AZURE_*` variables in `.env`.

**Q: The output JSON didn't parse correctly — I see a "raw" key.**  
A: The LLM occasionally produces non-JSON output. The raw text is preserved in the `raw` field. Try re-submitting with a clearer idea description.

**Q: Where are the API docs?**  
A: `http://localhost:8000/docs` (Swagger UI) or `http://localhost:8000/redoc` (ReDoc).
