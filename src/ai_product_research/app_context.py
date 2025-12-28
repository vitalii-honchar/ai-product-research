from dataclasses import dataclass

from langchain_core.language_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from ai_product_research.agents import ProblemRetrieverAgent
from ai_product_research.services import AnalyzedProductTelegramChannelService
from ai_product_research.services.product_hunt import ProductHuntService
from ai_product_research.services.web_site_scrapper import WebSiteScrapperService
from ai_product_research.settings.settings import init_app_settings, AppSettings
from ai_product_research.usecase import TelegramProductsResearchUseCase


@dataclass
class AppContext:
    gemini3_flash: BaseChatModel
    chatgpt_5_mini: BaseChatModel
    product_hunt_service: ProductHuntService
    scraper_service: WebSiteScrapperService
    settings: AppSettings
    problem_retriever_agent: ProblemRetrieverAgent
    telegram_product_research_use_case: TelegramProductsResearchUseCase
    analyzed_products_telegram_channel_service: AnalyzedProductTelegramChannelService


def create_app_context() -> AppContext:
    settings = init_app_settings()
    product_hunt_service = ProductHuntService(settings.product_hunt_dev_token)
    scraper_service = WebSiteScrapperService(timeout=30000)

    gemini3_flesh_model = ChatGoogleGenerativeAI(
        model="gemini-3-flash-preview",
        temperature=0,
        max_tokens=1024,
        max_retries=2,
        api_key=settings.google_api_key,
    )
    chatgpt_5_mini = ChatOpenAI(
        model="gpt-5-mini",
        temperature=0,
        max_tokens=4096,
        max_retries=2,
        api_key=settings.openai_api_key,
    )

    problem_retriever_agent = ProblemRetrieverAgent(gemini3_flesh_model)
    analyzed_products_telegram_channel_service = AnalyzedProductTelegramChannelService(
        channel_id=settings.telegram_channel_id,
        telegram_bot_token=settings.telegram_bot_token,
    )

    return AppContext(
        gemini3_flash=gemini3_flesh_model,
        chatgpt_5_mini=chatgpt_5_mini,
        product_hunt_service=product_hunt_service,
        scraper_service=scraper_service,
        settings=settings,
        problem_retriever_agent=problem_retriever_agent,
        telegram_product_research_use_case=TelegramProductsResearchUseCase(
            product_hunt_service=product_hunt_service,
            problem_retriever_agent=problem_retriever_agent,
            scraper_service=scraper_service,
            analyzed_products_telegram_channel_service=analyzed_products_telegram_channel_service,
        ),
        analyzed_products_telegram_channel_service=analyzed_products_telegram_channel_service,
    )
