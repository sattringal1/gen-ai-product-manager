import json
from langchain_core.messages import HumanMessage, SystemMessage
from agents.base import BaseAgent
from models.schemas import VisionStatement

SYSTEM_PROMPT = """You are a Chief Product Officer. Given a product idea, craft a compelling product vision.
Return ONLY valid JSON:
{
  "vision": "string (inspiring 1-sentence future state)",
  "mission": "string (how you achieve the vision)",
  "strategic_narrative": "string (3-5 sentences compelling story)",
  "target_audience": "string",
  "differentiators": ["string", ...]
}
The vision must be aspirational (5-10 year horizon). Mission must be actionable. Min 3 differentiators."""


class Visionary(BaseAgent):
    name = "visionary"

    async def run(self, idea: str) -> tuple[dict, str]:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Product idea: {idea}"),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content
        try:
            data = json.loads(raw)
            vision = VisionStatement(**data)
            return vision.model_dump(), raw
        except Exception:
            return {"raw": raw}, raw
