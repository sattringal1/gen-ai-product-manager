import json
from langchain_core.messages import HumanMessage, SystemMessage
from agents.base import BaseAgent
from models.schemas import OKRSet

SYSTEM_PROMPT = """You are a seasoned OKR coach. Given a product idea, define a focused OKR set.
Return ONLY valid JSON:
{
  "okrs": [
    {
      "objective": "string (qualitative, inspiring)",
      "key_results": ["string (measurable, time-bound)", ...],
      "timeframe": "string (e.g., Q1 2026)"
    }
  ],
  "north_star_metric": "string (the single most important metric)"
}
Produce 3-4 objectives, each with 3 key results. KRs must have numbers/percentages."""


class OKRStrategist(BaseAgent):
    name = "okr_strategist"

    async def run(self, idea: str) -> tuple[dict, str]:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Product idea: {idea}"),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content
        try:
            data = json.loads(raw)
            okrs = OKRSet(**data)
            return okrs.model_dump(), raw
        except Exception:
            return {"raw": raw}, raw
