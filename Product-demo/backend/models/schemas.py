from pydantic import BaseModel, Field
from typing import Optional, Literal, Any
from enum import Enum


class AgentType(str, Enum):
    LEAN_IDEA_ARCHITECT = "lean_idea_architect"
    BUSINESS_MODELER = "business_modeler"
    VALUE_PROPOSITION_DESIGNER = "value_proposition_designer"
    VISIONARY = "visionary"
    OKR_STRATEGIST = "okr_strategist"
    ROADMAP_PLANNER = "roadmap_planner"
    USER_STORY_TELLER = "user_story_teller"
    AUTO = "auto"


class ProcessRequest(BaseModel):
    idea: str = Field(..., min_length=10, max_length=5000, description="The product idea or prompt")
    agent: AgentType = Field(AgentType.AUTO, description="Which agent to invoke; AUTO lets orchestrator decide")
    push_to_jira: bool = Field(False, description="Push user stories to Jira on completion")
    push_to_confluence: bool = Field(False, description="Publish output to Confluence on completion")
    jira_project_key: Optional[str] = None
    confluence_space_key: Optional[str] = None


class LeanCanvas(BaseModel):
    problem: list[str]
    customer_segments: list[str]
    unique_value_proposition: str
    solution: list[str]
    channels: list[str]
    revenue_streams: list[str]
    cost_structure: list[str]
    key_metrics: list[str]
    unfair_advantage: str


class BusinessModelCanvas(BaseModel):
    key_partners: list[str]
    key_activities: list[str]
    key_resources: list[str]
    value_propositions: list[str]
    customer_relationships: list[str]
    channels: list[str]
    customer_segments: list[str]
    cost_structure: list[str]
    revenue_streams: list[str]


class ValueProposition(BaseModel):
    customer_jobs: list[str]
    pains: list[str]
    gains: list[str]
    pain_relievers: list[str]
    gain_creators: list[str]
    products_services: list[str]


class VisionStatement(BaseModel):
    vision: str
    mission: str
    strategic_narrative: str
    target_audience: str
    differentiators: list[str]


class OKR(BaseModel):
    objective: str
    key_results: list[str]
    timeframe: str


class OKRSet(BaseModel):
    okrs: list[OKR]
    north_star_metric: str


class RoadmapPhase(BaseModel):
    phase: str
    duration: str
    goals: list[str]
    deliverables: list[str]
    dependencies: list[str]


class Roadmap(BaseModel):
    phases: list[RoadmapPhase]
    total_duration: str
    success_criteria: list[str]


class AcceptanceCriteria(BaseModel):
    given: str
    when: str
    then: str


class UserStory(BaseModel):
    title: str
    as_a: str
    i_want: str
    so_that: str
    acceptance_criteria: list[AcceptanceCriteria]
    story_points: int
    priority: Literal["Critical", "High", "Medium", "Low"]
    labels: list[str]
    epic: Optional[str] = None


class UserStorySet(BaseModel):
    epic_name: str
    epic_summary: str
    stories: list[UserStory]


class AgentResult(BaseModel):
    agent: AgentType
    idea: str
    output: Any
    raw_text: str
    jira_issue_keys: list[str] = []
    confluence_page_url: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    llm_provider: str
