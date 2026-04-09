from abc import ABC, abstractmethod
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from config import settings
import structlog

log = structlog.get_logger()


def get_llm() -> BaseChatModel:
    if settings.llm_provider == "azure_openai":
        return AzureChatOpenAI(
            azure_endpoint=settings.azure_openai_endpoint,
            azure_deployment=settings.azure_openai_deployment,
            api_version=settings.azure_openai_api_version,
            api_key=settings.azure_openai_api_key,
            temperature=0.7,
        )
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0.7,
    )


class BaseAgent(ABC):
    name: str = "base"

    def __init__(self):
        self.llm = get_llm()
        self.log = structlog.get_logger(agent=self.name)

    @abstractmethod
    async def run(self, idea: str) -> tuple[dict, str]:
        """Returns (structured_output, raw_text)."""
        ...
