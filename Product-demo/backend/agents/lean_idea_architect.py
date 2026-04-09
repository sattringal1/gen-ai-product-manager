import json
from langchain_core.messages import HumanMessage, SystemMessage
from agents.base import BaseAgent
from models.schemas import LeanCanvas

SYSTEM_PROMPT = """You are a Lean Startup expert. Given a product idea, produce a complete Lean Canvas.
Return ONLY valid JSON matching this schema:
{
  "problem": ["string", ...],
  "customer_segments": ["string", ...],
  "unique_value_proposition": "string",
  "solution": ["string", ...],
  "channels": ["string", ...],
  "revenue_streams": ["string", ...],
  "cost_structure": ["string", ...],
  "key_metrics": ["string", ...],
  "unfair_advantage": "string"
}
Be concise, specific, and actionable. Minimum 3 items per list field."""


class LeanIdeaArchitect(BaseAgent):
    name = "lean_idea_architect"

    async def run(self, idea: str) -> tuple[dict, str]:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Product idea: {idea}"),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content
        try:
            data = json.loads(raw)
            canvas = LeanCanvas(**data)
            return canvas.model_dump(), raw
        except Exception:
            # Return raw text in structured form if parsing fails
            return {"raw": raw}, raw
