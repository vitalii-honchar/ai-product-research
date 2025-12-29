from dataclasses import dataclass

from ai_product_research.agents.product_filter_agent import ProductFilterAgent
from ai_product_research.domain import AnalyzedProduct, BusinessProblem


@dataclass
class ProductTestCase:
    """Test case containing a product and its expected filter result"""
    product: AnalyzedProduct
    expected_passed: bool


# Test data: Products with expected filter results
TEST_PRODUCTS = [
    ProductTestCase(
        product=AnalyzedProduct(
            origin_url='https://www.producthunt.com/products/vibrantsnap?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            product_url='https://www.producthunt.com/r/QRNRG4XPPKNIW4?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            name='VibrantSnap',
            problem=BusinessProblem(
                primary_customer='SaaS founders, sales teams, and content creators who need to create professional product demos and outreach videos.',
                core_job='Create, edit, and share high-quality screen recordings and product demos to convert viewers into customers.',
                main_pain='Existing video recording tools are often complicated and time-consuming, requiring manual editing to look professional and drive results.',
                success_metric='Convert viewers into customers faster and increase prospect engagement rates through professional-quality outreach videos.'
            )
        ),
        expected_passed=False
    ),
    ProductTestCase(
        product=AnalyzedProduct(
            origin_url='https://www.producthunt.com/products/tweny-eye-health-focus-timer?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            product_url='https://www.producthunt.com/r/PVKRQH5BY6FT4K?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            name='Tweny',
            problem=BusinessProblem(
                primary_customer='Tech-savvy individuals and software developers looking for niche health and productivity tools.',
                core_job='Improve personal well-being and streamline technical workflows through a suite of specialized applications.',
                main_pain='Mainstream applications are often too broad or lack privacy, failing to provide focused solutions for specific needs like eye-strain prevention or local AI assistance.',
                success_metric='Achieve 100% adherence to healthy work-rest habits and reduce time spent on technical configurations through automated utility tools.'
            )
        ),
        expected_passed=False
    ),
    ProductTestCase(
        product=AnalyzedProduct(
            origin_url='https://www.producthunt.com/products/hmpl-js?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            product_url='https://www.producthunt.com/r/NTQB24QGO7GL5Z?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            name='HMPL',
            problem=BusinessProblem(
                primary_customer='JavaScript developers and web development teams building modern, server-oriented web applications.',
                core_job='Fetch and render server-oriented HTML templates safely to keep web applications dynamic and lightweight.',
                main_pain='Building dynamic interfaces often leads to bloated bundle sizes and security risks like XSS when managing server-side template interactions.',
                success_metric='Reduce application bundle size by up to 1.67x while maintaining 100% code coverage and built-in XSS protection.'
            )
        ),
        expected_passed=False
    ),
    ProductTestCase(
        product=AnalyzedProduct(
            origin_url='https://www.producthunt.com/products/kardy?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            product_url='https://www.producthunt.com/r/HYX6TWP2XDD2GY?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            name='Kardy',
            problem=BusinessProblem(
                primary_customer='Individuals, families, and business teams, particularly those working in remote or distributed environments.',
                core_job='Create, customize, and coordinate collaborative digital greeting cards for group celebrations and occasions.',
                main_pain='Physical group cards are expensive, wasteful, and difficult to circulate for signatures among remote or geographically dispersed people.',
                success_metric='Reduce card costs by up to 60% and eliminate the time spent manually chasing individuals for signatures through automated digital coordination.'
            )
        ),
        expected_passed=False
    ),
    ProductTestCase(
        product=AnalyzedProduct(
            origin_url='https://www.producthunt.com/products/linkeddit?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            product_url='https://www.producthunt.com/r/XCDD25OB34XNR2?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            name='Linkeddit',
            problem=BusinessProblem(
                primary_customer='Sales teams, marketers, and recruiters looking to find high-intent leads or talent within Reddit communities.',
                core_job='Identify and engage with potential customers by automatically scanning Reddit conversations for high-intent signals.',
                main_pain='Manually searching and scrolling through subreddits to find qualified leads is labor-intensive and results in low-converting outreach.',
                success_metric='Discover and export high-value Reddit leads in under 5 minutes and eliminate hours of manual research through 24/7 automated scanning.'
            )
        ),
        expected_passed=True
    ),
    ProductTestCase(
        product=AnalyzedProduct(
            origin_url='https://www.producthunt.com/products/optivault-ai-financial-advisor-app?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            product_url='https://www.producthunt.com/r/LIFDVKRN6E3RIH?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            name='Optivault',
            problem=BusinessProblem(
                primary_customer='iOS users seeking a centralized and automated way to manage their personal finances, including bank accounts, credit cards, and crypto wallets.',
                core_job='Provide an AI-driven personal financial advisor to sync various financial accounts and optimize spending to grow net worth.',
                main_pain='Managing fragmented financial data across multiple platforms makes it difficult to track spending and identify opportunities for growing personal wealth.',
                success_metric='Increase net worth and optimize spending efficiency through automated, AI-powered financial insights and goal tracking.'
            )
        ),
        expected_passed=True
    ),
    ProductTestCase(
        product=AnalyzedProduct(
            origin_url='https://www.producthunt.com/products/meetings-wrapped?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            product_url='https://www.producthunt.com/r/BW423JWAEPSG3Z?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            name='Meetings Wrapped',
            problem=BusinessProblem(
                primary_customer='Corporate professionals and team leads who use digital calendars to manage their daily work schedules.',
                core_job='Analyze and visualize annual meeting data from synced calendars to provide a year-end performance summary.',
                main_pain='A lack of visibility into how much time is wasted on unproductive meetings that could have been handled through asynchronous communication.',
                success_metric='Quantify and visualize hundreds of hours of meeting time to help users identify and reclaim productive work hours.'
            )
        ),
        expected_passed=False
    ),
    ProductTestCase(
        product=AnalyzedProduct(
            origin_url='https://www.producthunt.com/products/standby-mode-pro?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            product_url='https://www.producthunt.com/r/WICUE6RY65SO27?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            name='StandBy Mode Pro',
            problem=BusinessProblem(
                primary_customer='Android smartphone users who want to repurpose their device as a functional desk or nightstand smart display while it is charging.',
                core_job='Transform a charging smartphone into a customizable, glanceable smart display that shows real-time widgets and information.',
                main_pain='Smartphones are typically idle and non-functional while charging, requiring users to manually wake the device to check the time, weather, or notifications.',
                success_metric='View key information from a distance without physical interaction and reduce the frequency of waking the device for status checks by 80% during charging sessions.'
            )
        ),
        expected_passed=False
    ),
    ProductTestCase(
        product=AnalyzedProduct(
            origin_url='https://www.producthunt.com/products/monee?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            product_url='https://www.producthunt.com/r/ISQ2N3CZCMAPGL?utm_campaign=producthunt-api&utm_medium=api-v2&utm_source=Application%3A+product-hunt-cli+%28ID%3A+252374%29',
            name='Monee',
            problem=BusinessProblem(
                primary_customer='Individuals, families, and roommates who need to coordinate and track personal or shared household finances.',
                core_job='Track and categorize income and expenses to maintain a clear overview of financial transactions and budgets.',
                main_pain='Lack of control over finances and the difficulty of tracking shared spending without intrusive ads or subscription fees.',
                success_metric='Gain instant visibility into monthly spending through insightful summaries and reduce manual logging time to seconds per entry.'
            )
        ),
        expected_passed=False
    ),
]


class TestProductFilterAgent:
    async def test_filters_products_with_high_accuracy(self, product_filter_agent: ProductFilterAgent):
        """
        Test that ProductFilterAgent correctly filters AI-powered products.

        The agent should:
        1. PASS products that use LLM/AI capabilities
        2. FAIL products without AI features
        3. Consider revenue potential ($10K+ MRR)
        4. Filter for real human problems

        Success criteria: >= 75% accuracy across all test cases
        """
        # given
        accuracy_threshold = 0.75
        correct_count = 0
        total_count = len(TEST_PRODUCTS)

        results = []

        # when - filter each product
        for test_case in TEST_PRODUCTS:
            actual_passed = await product_filter_agent.filter_product(test_case.product)
            is_correct = (actual_passed == test_case.expected_passed)

            if is_correct:
                correct_count += 1

            results.append({
                'name': test_case.product.name,
                'expected': test_case.expected_passed,
                'actual': actual_passed,
                'correct': is_correct
            })

        # Calculate accuracy
        accuracy = correct_count / total_count

        # Build detailed error message
        error_details = f"\n\nFiltering Accuracy: {accuracy:.2%} ({correct_count}/{total_count})\n\n"
        error_details += "Individual Results:\n"
        error_details += "-" * 80 + "\n"

        for result in results:
            status = "PASS" if result['correct'] else "FAIL"
            error_details += f"[{status}] {result['name']:20} | Expected: {str(result['expected']):5} | Actual: {str(result['actual']):5}\n"

        # then
        assert accuracy >= accuracy_threshold, (
            f"Filter accuracy {accuracy:.2%} is below threshold {accuracy_threshold:.0%}."
            f"{error_details}"
        )
