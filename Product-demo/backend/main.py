import structlog
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from models.schemas import ProcessRequest, AgentResult, HealthResponse, AgentType
from agents.orchestrator import Orchestrator

log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("startup", env=settings.app_env, llm=settings.llm_provider)
    yield
    log.info("shutdown")


app = FastAPI(
    title="Gen-AI Product Manager API",
    version="1.0.0",
    description="Multi-agent AI system that transforms product ideas into actionable strategy artifacts.",
    lifespan=lifespan,
)

_cors_origins = settings.cors_origins_list
# In production allow all origins if none explicitly configured
if settings.app_env == "production" and not _cors_origins:
    _cors_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_cors_origins if "*" not in _cors_origins else ["*"],
    allow_origin_regex=r"https://.*\.azurecontainerapps\.io" if settings.app_env == "production" else None,
    allow_credentials="*" not in _cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = Orchestrator()


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health():
    return HealthResponse(status="ok", version="1.0.0", llm_provider=settings.llm_provider)


@app.post("/api/v1/process", response_model=AgentResult, tags=["Agents"])
async def process_idea(req: ProcessRequest):
    """
    Main entry point. Accepts a product idea and optional agent override.
    Returns the structured output from the selected agent.
    """
    try:
        result = await orchestrator.run(req)
        return result
    except Exception as exc:
        log.error("process_failed", error=str(exc))
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/api/v1/agents", tags=["Agents"])
async def list_agents():
    """Return metadata for all available agents."""
    return {
        "agents": [
            {"id": "lean_idea_architect", "name": "Lean Idea Architect", "description": "Creates Lean Canvas structures from raw ideas"},
            {"id": "business_modeler", "name": "Business Modeler", "description": "Produces Business Model Canvas output"},
            {"id": "value_proposition_designer", "name": "Value Proposition Designer", "description": "Maps customer needs to product capabilities"},
            {"id": "visionary", "name": "Visionary", "description": "Creates vision statements and strategic narratives"},
            {"id": "okr_strategist", "name": "OKR Strategist", "description": "Defines measurable OKRs aligned to the product"},
            {"id": "roadmap_planner", "name": "Roadmap Planner", "description": "Builds phased outcome-driven product roadmaps"},
            {"id": "user_story_teller", "name": "User Story Teller", "description": "Generates Jira-ready user stories with acceptance criteria"},
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=settings.app_port, reload=True)
