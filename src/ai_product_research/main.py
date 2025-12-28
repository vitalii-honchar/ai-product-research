import asyncio
import logging
from datetime import datetime

from ai_product_research.app_context import create_app_context

log = logging.getLogger(__name__)


async def main():
    ctx = create_app_context()
    target_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    await ctx.telegram_product_research_use_case.execute(target_date)


if __name__ == "__main__":
    asyncio.run(main())