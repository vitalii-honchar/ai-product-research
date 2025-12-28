from pydantic import BaseModel, Field
from typing import Optional
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
import logging
import base64

log = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are product manager who specializes in the analysis of an existing products.
Your task is to analyze provided product from the screenshot and retrieve data:
- primary_customer - the primary customer(s) of this business.
- core_job - the core job which product is doing. Should be one specific job.
- main_pain - the main customer pain which product is solving. Should be one specific pain.
- success_metric - the success metric of this business. MUST be a measurable OUTCOME (faster, more, improved, reduced), NOT a product feature or pricing.

CRITICAL: success_metric should describe the RESULT the customer achieves, not what the product offers.
- GOOD: "Book 50% more meetings", "Reduced scheduling time by 3 hours per week", "Improved team productivity"
- BAD: "Manage 3 booking pages", "$9 one-time payment", "Access to premium features"

Restrictions:
- Strictly retrieve information from the screenshot without generating additional information.
- Provide professional and concise description of retrieved information.

Example 1 (Video editing platform):
- primary_customer: Content creators and social media marketers who produce short-form videos.
- core_job: Edit and produce professional-quality short videos quickly.
- main_pain: Traditional video editing software has a steep learning curve and takes hours to produce simple clips.
- success_metric: Reduce video production time from 2 hours to 15 minutes and increase content output by 5x.

Example 2 (Sales CRM):
- primary_customer: B2B sales teams and account executives managing complex deals.
- core_job: Track and manage customer relationships throughout the sales pipeline.
- main_pain: Sales data scattered across spreadsheets and emails makes it hard to prioritize high-value opportunities.
- success_metric: Close 40% more deals by surfacing actionable insights and automating follow-up tasks.

Example 3 (Project management platform):
- primary_customer: Remote teams and project managers coordinating distributed workforces.
- core_job: Coordinate team tasks and track project progress in real-time.
- main_pain: Team members miss deadlines because visibility into task dependencies and blockers is poor.
- success_metric: Deliver projects 30% faster with 50% fewer missed deadlines through improved visibility."""

class BusinessProblem(BaseModel):
    primary_customer: str = Field(description="Primary customer of this business", max_length=512, min_length=1)
    core_job: str = Field(description="Core job of this business", max_length=512, min_length=1)
    main_pain: str = Field(description="Main pain of this business", max_length=512, min_length=1)
    success_metric: str = Field(description="Success metric of this business", max_length=512, min_length=1)


class ProblemRetrieverAgent:

    def __init__(self, chat_model: BaseChatModel):
        self.llm = chat_model.with_structured_output(BusinessProblem)

    async def retrieve_problem(self, website_screenshot: bytes) -> BusinessProblem | None:
        # Encode screenshot to base64
        screenshot_base64 = base64.standard_b64encode(website_screenshot).decode("utf-8")

        # Create messages
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(
                content=[
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"},
                    },
                    {
                        "type": "text",
                        "text": "Analyze this website screenshot and identify the primary customer, core job they're trying to accomplish, main pain point, and success metric for this business.",
                    },
                ]
            )
        ]

        # Call LLM with structured output
        log.info("Calling LLM to analyze screenshot")
        result = await self.llm.ainvoke(messages)
        log.info("Retrieved business problem: %s", result)

        return result

