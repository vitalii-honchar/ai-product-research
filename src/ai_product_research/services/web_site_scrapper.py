import logging
from typing import Optional
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
import httpx

log = logging.getLogger(__name__)


class WebSiteScrapperService:
    def __init__(self, timeout: int = 30000):
        """
        Initialize the web scraper service.

        Args:
            timeout: Timeout in milliseconds for page load (default: 30000ms = 30s)
        """
        self.timeout = timeout

    async def _resolve_redirects(self, url: str) -> Optional[str]:
        """
        Follow redirects to get the final URL.

        Args:
            url: The URL that may redirect

        Returns:
            The final URL after following redirects, or None if failed
        """
        try:
            async with httpx.AsyncClient(follow_redirects=True, timeout=10.0) as client:
                # Use GET with stream to avoid downloading full content
                async with client.stream("GET", url) as response:
                    final_url = str(response.url)
                    log.info(f"Resolved {url[:80]}... -> {final_url}")
                    return final_url
        except Exception as e:
            log.warning(f"Failed to resolve redirects for {url[:80]}...: {e}")
            return url  # Return original URL if redirect resolution fails

    async def scrape(self, url: str) -> Optional[bytes]:
        """
        Scrape a website and return a full-page screenshot.
        Uses Playwright with Chromium to render React/SPA sites.

        Args:
            url: The URL to scrape

        Returns:
            Screenshot bytes (PNG format) of the full page, or None if scraping fails
        """
        try:
            async with async_playwright() as p:
                # Launch browser with args to appear more like a real browser
                browser = await p.chromium.launch(
                    headless=True,
                    args=['--disable-blink-features=AutomationControlled']
                )

                # Create context with realistic settings
                context = await browser.new_context(
                    user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                    viewport={'width': 1920, 'height': 1080}
                )

                page = await context.new_page()

                # Remove webdriver detection
                await page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    })
                """)

                log.info(f"Scraping {url[:80]}...")

                # Navigate to the page and let Playwright handle redirects
                await page.goto(url, timeout=self.timeout, wait_until="domcontentloaded")

                # Wait for navigation to complete (handles JS redirects)
                try:
                    # Wait up to 5 seconds for potential JavaScript redirects
                    await page.wait_for_load_state("networkidle", timeout=5000)
                except Exception:
                    # If no additional navigation happens, that's fine
                    pass

                # Get the final URL after all redirects
                final_url = page.url
                log.info(f"Final URL: {final_url[:80]}...")

                # Wait a bit for any dynamic content to load
                await page.wait_for_timeout(2000)

                # Take a full-page screenshot
                screenshot_bytes = await page.screenshot(full_page=True, type='png')

                await context.close()
                await browser.close()

                log.info(f"Successfully scraped {final_url[:80]}... - screenshot size: {len(screenshot_bytes)} bytes")
                return screenshot_bytes

        except PlaywrightTimeoutError:
            log.warning(f"Timeout while scraping {url[:80]}...")
            return None
        except Exception as e:
            log.error(f"Error scraping {url[:80]}...: {str(e)}")
            return None
