from langchain_core.language_models import BaseChatModel
from ai_product_research.agents import ProblemRetrieverAgent
from ai_product_research.app_context import create_app_context, AppContext
import pytest

@pytest.fixture
def app_context() -> AppContext:
    return create_app_context()

@pytest.fixture
def problem_retriever_agent(app_context: AppContext) -> ProblemRetrieverAgent:
    return app_context.problem_retriever_agent

@pytest.fixture
def chatgpt_5_mini(app_context: AppContext) -> BaseChatModel:
    return app_context.chatgpt_5_mini
