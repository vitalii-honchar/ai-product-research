import logging
from dataclasses import dataclass

import httpx

from ai_product_research.domain import AnalyzedProduct

logger = logging.getLogger(__name__)


@dataclass
class AnalyzedProductTelegramChannelService:
    TELEGRAM_MESSAGE_LIMIT = 4096

    channel_id: str
    telegram_bot_token: str

    async def send_updates(self, products: list[AnalyzedProduct]) -> None:
        if not products:
            logger.info("No products to send")
            return

        logger.info(f"Sending {len(products)} product(s) to Telegram channel {self.channel_id}")

        batched_messages = self._batch_products_into_messages(products)

        for i, message in enumerate(batched_messages, 1):
            await self._send_message(message)
            logger.info(f"Sent message batch {i}/{len(batched_messages)}")

    def _batch_products_into_messages(self, products: list[AnalyzedProduct]) -> list[str]:
        messages = []
        current_message_parts = []
        separator = "\n\n───\n\n"

        for product in products:
            product_text = self._format_product_message(product)

            if current_message_parts:
                test_message = separator.join(current_message_parts + [product_text])
            else:
                test_message = product_text

            if len(test_message) > self.TELEGRAM_MESSAGE_LIMIT and current_message_parts:
                messages.append(separator.join(current_message_parts))
                current_message_parts = []

            current_message_parts.append(product_text)

        if current_message_parts:
            messages.append(separator.join(current_message_parts))

        return messages

    def _format_product_message(self, product: AnalyzedProduct) -> str:
        name = self._escape_markdown(product.name)
        customer = self._escape_markdown(product.problem.primary_customer)
        job = self._escape_markdown(product.problem.core_job)
        pain = self._escape_markdown(product.problem.main_pain)
        metric = self._escape_markdown(product.problem.success_metric)

        return f"""🚀 *{name}*

👥 *Customer:* {customer}
💼 *Job to be Done:* {job}
⚡ *Pain Point:* {pain}
📊 *Success Metric:* {metric}

🔗 *Links:*
• [Product Website]({product.product_url})
• [Original Source]({product.origin_url})"""

    async def _send_message(self, text: str) -> None:
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"

        payload = {
            "chat_id": self.channel_id,
            "text": text,
            "parse_mode": "MarkdownV2",
            "disable_web_page_preview": False,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=10.0)

                if response.status_code != 200:
                    logger.error(f"Telegram API HTTP error: {response.status_code} - {response.text}")
                    return

                result = response.json()
                if not result.get("ok"):
                    error_description = result.get("description", "Unknown error")
                    logger.error(f"Telegram API error: {error_description}")
        except Exception as e:
            logger.error(f"Failed to send message to Telegram: {e}", exc_info=True)

    @staticmethod
    def _escape_markdown(text: str) -> str:
        special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        for char in special_chars:
            text = text.replace(char, f'\\{char}')
        return text
