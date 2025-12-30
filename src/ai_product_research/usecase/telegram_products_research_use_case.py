import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from ai_product_research.agents import ProblemRetrieverAgent, ProductFilterAgent
from ai_product_research.domain import ProductHuntPost, AnalyzedProduct, BusinessProblem
from ai_product_research.services import ProductHuntService, WebSiteScrapperService, \
    AnalyzedProductTelegramChannelService

log = logging.getLogger(__name__)

POSTS_LIMIT = 3


@dataclass
class TelegramProductsResearchUseCase:
    product_hunt_service: ProductHuntService
    problem_retriever_agent: ProblemRetrieverAgent
    scraper_service: WebSiteScrapperService
    analyzed_products_telegram_channel_service: AnalyzedProductTelegramChannelService
    product_filter_agent: ProductFilterAgent

    async def execute(self, target_date: datetime) -> None:
        log.info(f"Start executing telegram products research use case: target_date = {target_date}")
        next_day = target_date + timedelta(days=1)
        posts = await self.product_hunt_service.get_posts(posted_after=target_date, posted_before=next_day)
        filtered_posts: list[AnalyzedProduct] = []
        top_posts: list[AnalyzedProduct] = []
        for post in posts:
            if len(filtered_posts) >= POSTS_LIMIT:
                break
            analyzed_post = await self.analyze_post(post)
            if analyzed_post is not None:
                if len(top_posts) < POSTS_LIMIT:
                    top_posts.append(analyzed_post)
                filter_passed = await self.product_filter_agent.filter_product(analyzed_post)
                log.info(f"Product filter: {analyzed_post.name} passed={filter_passed}")
                if filter_passed:
                    filtered_posts.append(analyzed_post)

        for post in top_posts:
            if len(filtered_posts) >= POSTS_LIMIT:
                break
            filtered_posts.append(post)

        log.info(f"Analyzed posts: posts = {filtered_posts}")
        await self.analyzed_products_telegram_channel_service.send_updates(filtered_posts)

    async def analyze_post(self, post: ProductHuntPost) -> AnalyzedProduct | None:
        log.info(f"Start analyzing post: post = {post}")
        try:
            screenshot_bytes = await self.scraper_service.scrape(post.website)
            business_problem = await self.problem_retriever_agent.retrieve_problem(screenshot_bytes)
            return AnalyzedProduct(
                origin_url=post.url,
                product_url=post.website,
                name=post.name,
                problem=BusinessProblem.model_validate(business_problem.model_dump()),
            )
        except Exception:
            log.error(f"Error during analyzing a post: post = {post}", exc_info=True)
            return None
