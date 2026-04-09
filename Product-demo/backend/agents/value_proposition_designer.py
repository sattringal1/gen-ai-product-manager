import json
from langchain_core.messages import HumanMessage, SystemMessage
from agents.base import BaseAgent
from models.schemas import ValueProposition

SYSTEM_PROMPT = """You are a Value Proposition Design expert (Osterwalder methodology).
Given a product idea, create a detailed Value Proposition Canvas.
Return ONLY valid JSON:
{
  "customer_jobs": ["string", ...],
  "pains": ["string", ...],
  "gains": ["string", ...],
  "pain_relievers": ["string", ...],
  "gain_creators": ["string", ...],
  "products_services": ["string", ...]
}
Map each pain to a pain reliever and each gain to a gain creator. Min 4 items each."""


class ValuePropositionDesigner(BaseAgent):
    name = "value_proposition_designer"

    async def run(self, idea: str) -> tuple[dict, str]:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=f"Product idea: {idea}"),
        ]
        response = await self.llm.ainvoke(messages)
        raw = response.content
        try:
            data = json.loads(raw)
            vp = ValueProposition(**data)
            return vp.model_dump(), raw
        except Exception:
            return {"raw": raw}, raw
