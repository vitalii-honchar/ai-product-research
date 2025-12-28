import asyncio
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta

from ai_product_research.agents import ProblemRetrieverAgent
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

    async def execute(self, target_date: datetime) -> None:
        log.info(f"Start executing telegram products research use case: target_date = {target_date}")
        next_day = target_date + timedelta(days=1)
        posts = await self.product_hunt_service.get_posts(posted_after=target_date, posted_before=next_day,
                                                          limit=POSTS_LIMIT)
        posts_stream = filter(lambda p: p is not None, map(self.analyze_post, posts))
        analyzed_posts = await asyncio.gather(*posts_stream)
        log.info(f"Analyzed posts: posts = {analyzed_posts}")
        await self.analyzed_products_telegram_channel_service.send_updates(analyzed_posts)

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
        except Exception as e:
            log.error(f"Error during analyzing a post: post = {post}", exc_info=True)
            return None
