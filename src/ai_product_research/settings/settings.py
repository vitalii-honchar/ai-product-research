import logging

from pydantic_settings import BaseSettings
from rich.console import Console
from rich.logging import RichHandler


class AppSettings(BaseSettings):
    openai_api_key: str
    model_name: str = "gpt-5.2"
    telegram_bot_token: str
    telegram_channel_id: str
    debug: bool = False
    product_hunt_api_key: str
    product_hunt_api_secret: str
    product_hunt_dev_token: str
    google_api_key: str

    class Config:
        env_file = ".env"
        env_prefix = "AI_PRODUCT_RESEARCH_"
        extra = "allow"

def init_app_settings() -> AppSettings:
    settings = AppSettings() # type: ignore

    if settings.debug:
        console = Console(width=200, force_terminal=True, color_system="auto")
        logging.basicConfig(
            level=logging.INFO,
            format="%(message)s",
            handlers=[RichHandler(
                rich_tracebacks=True,
                markup=True,
                console=console,
                show_time=True,
                show_path=False,
            )]
        )
    else:
        logging.basicConfig(level=logging.INFO)

    return settings