import json
from langchain_core.messages import HumanMessage, SystemMessage
from agents.base import BaseAgent
from models.schemas import BusinessModelCanvas

SYSTEM_PROMPT = """You are a Business Strategy expert. Given a product idea, produce a complete Business Model Canvas (BMC).
Return ONLY valid JSON matching:
{
  "key_partners": ["string", ...],
  "key_activities": ["string", ...],
  "key_resources": ["string", ...],
  "value_propositions": ["string", ...],
  "customer_relationships": ["string", ...],
  "channels": ["string", ...],
  "customer_segments": ["string", ...],
  "cost_structure": ["string", ...],
  "revenue_streams": ["string", ...]
}
Minimum 3 items per list. Be specific and enterprise-ready."""


class BusinessModeler(BaseAgent):
    name = "business_modeler"

    async def run(self, idea: str) -> tuple[dict, str]:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Product idea: {idea}"),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content
        try:
            data = json.loads(raw)
            canvas = BusinessModelCanvas(**data)
            return canvas.model_dump(), raw
        except Exception:
            return {"raw": raw}, raw
