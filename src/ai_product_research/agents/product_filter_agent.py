from langchain_core.language_models import BaseChatModel
from langchain_core.messages import SystemMessage, HumanMessage
from pydantic import BaseModel, Field

from ai_product_research.domain import AnalyzedProduct

SYSTEM_PROMPT = """You are product manager who specializes in the filtering not relevant software products.
Your task is to analyze provided product and decide if it matches requirements of a target product or not.
Product Requirements:
- Product should solve a problem with using LLM capabilities, ideally with Agentic AI.
- Product should solve real human problems, not imagine ones.
- Product should have a potential to earn at least $10K MRR.
"""


class FilterResult(BaseModel):
    passed: bool = Field(description="True if provided product matches requirements, otherwise False")


class ProductFilterAgent:
    def __init__(self, chat_model: BaseChatModel):
        self.llm = chat_model.with_structured_output(FilterResult)

    async def filter_product(self, product: AnalyzedProduct) -> bool:
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=product.model_dump_json())
        ]
        result = await self.llm.ainvoke(messages)
        return result.passed
