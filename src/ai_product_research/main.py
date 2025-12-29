import asyncio
import logging
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from ai_product_research.app_context import create_app_context

log = logging.getLogger(__name__)


async def main():
    ctx = create_app_context()
    cet_tz = ZoneInfo("Europe/Paris")
    last_execution_date = None

    if ctx.debug:
        target_date = (datetime.now(cet_tz) - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        await ctx.telegram_product_research_use_case.execute(target_date)

    while True:
        try:
            now_cet = datetime.now(cet_tz)
            if now_cet.hour == 6 and now_cet.minute == 0:
                target_date = (now_cet - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
                if last_execution_date != target_date.date():
                    log.info(f"Executing for target date: {target_date.date()}")
                    await ctx.telegram_product_research_use_case.execute(target_date)
                    last_execution_date = target_date.date()
                    log.info(f"Execution completed for {target_date.date()}")
            await asyncio.sleep(60)

        except Exception as e:
            log.error(f"Error in main loop: {e}", exc_info=True)
            await asyncio.sleep(60)


if __name__ == "__main__":
    asyncio.run(main())