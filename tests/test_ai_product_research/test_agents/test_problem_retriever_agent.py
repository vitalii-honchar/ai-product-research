from langchain_core.language_models import BaseChatModel
from ai_product_research.app_context import AppContext
from ai_product_research.agents.problem_retriever_agent import BusinessProblem, ProblemRetrieverAgent
from pathlib import Path
import pytest
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage, SystemMessage
import base64

class EvaluationResult(BaseModel):
    """Result of business problem evaluation"""
    score: float = Field(description="Success score between 0.0 and 1.0", ge=0.0, le=1.0)
    reasoning: str = Field(description="Explanation of the score")


class BusinessProblemEvaluator:
    """Evaluates if a retrieved BusinessProblem matches expectations using an LLM judge"""

    SYSTEM_PROMPT = """You are an expert evaluator judging business problem analyses using a GRADIENT SCORE from 0.0 to 1.0.

You will receive:
1. A screenshot of the product
2. EXPECTED analysis (JSON)
3. RETRIEVED analysis (JSON)

Your task: Calculate a final score from 0.0 to 1.0 based on semantic similarity across all 4 fields.

SCORING SYSTEM:
- 1.0 = Perfect match (same meaning across all fields)
- 0.75 = Good match (3 out of 4 fields match semantically)
- 0.5 = Partial match (2 out of 4 fields match semantically)
- 0.25 = Poor match (only 1 field matches)
- 0.0 = No match (completely different meanings across all fields)

CRITICAL RULES:
- DO NOT penalize for different wording, extra details, or rephrasing
- ONLY penalize if the core MEANING is different
- Each field contributes ~0.25 to the final score
- Calculate the final score by averaging how well each field matches

Evaluation criteria (each worth ~0.25):
1. primary_customer: Same target audience?
   - "developers" vs "software engineers" = 1.0 (same)
   - "developers" vs "developers and designers" = 0.9 (mostly same, slightly broader)
   - "developers" vs "marketers" = 0.0 (different)

2. core_job: Same main purpose?
   - "schedule meetings" vs "book appointments" = 1.0 (same)
   - "schedule meetings" vs "manage calendars" = 0.7 (related but different)
   - "schedule meetings" vs "analyze data" = 0.0 (different)

3. main_pain: Same problem being solved?
   - "wasting time" vs "time-consuming process" = 1.0 (same)
   - "wasting time" vs "manual effort required" = 0.8 (related)
   - "wasting time" vs "lack of features" = 0.0 (different)

4. success_metric: Both describe OUTCOMES (not features)?
   - "faster deployment" vs "reduced deployment time" = 1.0 (same outcome)
   - "increased bookings" vs "reduced scheduling time" = 0.9 (different but related outcomes - both valid)
   - "save time" vs "complete tasks faster" = 1.0 (same outcome, different words)
   - "increased revenue" vs "$9 pricing tier" = 0.0 (outcome vs feature)
   - "improved productivity" vs "access to 3 providers" = 0.0 (outcome vs feature)

   CRITICAL: As long as BOTH describe measurable outcomes (not features), score should be 0.8+
   Only penalize if one is a feature/pricing instead of an outcome.

Example scoring:
- 4/4 fields match semantically → Score: 1.0
- 3/4 fields match semantically → Score: 0.75
- 2/4 fields match semantically → Score: 0.5
- 1/4 fields match semantically → Score: 0.25
- 0/4 fields match semantically → Score: 0.0

Look at the screenshot to verify both analyses are grounded in what's visible."""

    def __init__(self, chat_model: BaseChatModel):
        self.llm = chat_model.with_structured_output(EvaluationResult)

    async def evaluate(
        self,
        actual: BusinessProblem,
        expected: BusinessProblem,
        screenshot_bytes: bytes
    ) -> EvaluationResult:
        """Evaluate how well the actual BusinessProblem matches the expected one"""
        # Encode screenshot to base64
        screenshot_base64 = base64.standard_b64encode(screenshot_bytes).decode("utf-8")

        # Build comparison text with JSON
        comparison_text = f"""EXPECTED:
{expected.model_dump_json()}

RETRIEVED:
{actual.model_dump_json()}"""

        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(
                content=[
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{screenshot_base64}"},
                    },
                    {
                        "type": "text",
                        "text": comparison_text,
                    },
                ]
            )
        ]

        # Call LLM with structured output
        result = await self.llm.ainvoke(messages)
        return result

# Pytest fixtures
@pytest.fixture
def evaluator(chatgpt_5_mini: BaseChatModel) -> BusinessProblemEvaluator:
    return BusinessProblemEvaluator(chatgpt_5_mini)


# Expected business problems for each screenshot
EXPECTED_TIMETUNA = BusinessProblem(
    primary_customer="Founders and startup teams who need to schedule meetings",
    core_job="Create professional branded scheduling pages that reflect their brand identity",
    main_pain="Generic booking pages look unprofessional and don't reflect their brand, reducing credibility",
    success_metric="Increased meeting bookings and improved brand perception from prospects"
)

EXPECTED_MONOCLE = BusinessProblem(
    primary_customer="Knowledge workers and creative professionals who work on computers",
    core_job="Create a distraction-free digital environment by blurring out background windows and desktop elements to isolate the active task",
    main_pain="Constant visual distractions from background applications that break concentration and prevent users from completing their intended tasks",
    success_metric="Improved focus and higher task completion rate with better recall"
)

EXPECTED_NETLIFY = BusinessProblem(
    primary_customer="Developers and engineering teams building applications",
    core_job="Integrate AI capabilities into their applications quickly and reliably",
    main_pain="Complex and time-consuming AI integration across different providers",
    success_metric="Faster AI integration with reduced implementation complexity and maintenance burden"
)


class TestProblemRetrieverAgent:

    @pytest.mark.parametrize("screenshot_filename,expected", [
        ("1_TimeTuna.png", EXPECTED_TIMETUNA),
        ("2_Monocle_3.0_for_macOS.png", EXPECTED_MONOCLE),
        ("3_Netlify_AI_Gateway.png", EXPECTED_NETLIFY),
    ])
    async def test_returns_correct_business_problem_if_screenshot_provided(
        self,
        problem_retriever_agent: ProblemRetrieverAgent,
        evaluator: BusinessProblemEvaluator,
        screenshot_filename: str,
        expected: BusinessProblem
    ):
        # given
        screenshot_path = Path(__file__).parent / "product_screenshots" / screenshot_filename
        screenshot_bytes = screenshot_path.read_bytes()
        threshold = 0.9

        # when
        actual = await problem_retriever_agent.retrieve_problem(screenshot_bytes)

        # then
        assert actual is not None, "Agent failed to retrieve business problem"

        # Evaluate using LLM judge
        evaluation = await evaluator.evaluate(actual, expected, screenshot_bytes)

        # Assert score meets threshold
        assert evaluation.score >= threshold, (
            f"Evaluation score {evaluation.score:.2f} is below threshold {threshold}.\n"
            f"Reasoning: {evaluation.reasoning}\n\n"
            f"Expected:\n"
            f"  Primary Customer: {expected.primary_customer}\n"
            f"  Core Job: {expected.core_job}\n"
            f"  Main Pain: {expected.main_pain}\n"
            f"  Success Metric: {expected.success_metric}\n\n"
            f"Actual:\n"
            f"  Primary Customer: {actual.primary_customer}\n"
            f"  Core Job: {actual.core_job}\n"
            f"  Main Pain: {actual.main_pain}\n"
            f"  Success Metric: {actual.success_metric}"
        )