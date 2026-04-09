import json
from langchain_core.messages import HumanMessage, SystemMessage
from agents.base import BaseAgent
from models.schemas import Roadmap

SYSTEM_PROMPT = """You are a Product Roadmap expert. Given a product idea, produce a phased outcome-driven roadmap.
Return ONLY valid JSON:
{
  "phases": [
    {
      "phase": "string (e.g., Phase 1: Foundation)",
      "duration": "string (e.g., Months 1-3)",
      "goals": ["string", ...],
      "deliverables": ["string", ...],
      "dependencies": ["string", ...]
    }
  ],
  "total_duration": "string",
  "success_criteria": ["string", ...]
}
Produce 4 phases (Foundation, Growth, Scale, Optimize). Each phase needs min 3 goals and 3 deliverables."""


class RoadmapPlanner(BaseAgent):
    name = "roadmap_planner"

    async def run(self, idea: str) -> tuple[dict, str]:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Product idea: {idea}"),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content
        try:
            data = json.loads(raw)
            roadmap = Roadmap(**data)
            return roadmap.model_dump(), raw
        except Exception:
            return {"raw": raw}, raw
