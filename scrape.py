from playwright.async_api import async_playwright
import random
import asyncio

# Optional: list of real user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
]

async def simulate_human_behavior(page):
    # Scroll down slowly
    scroll_times = random.randint(3, 6)
    for _ in range(scroll_times):
        scroll_height = random.randint(300, 700)
        await page.evaluate(f"window.scrollBy(0, {scroll_height})")
        await asyncio.sleep(random.uniform(0.5, 1.5))  # wait between scrolls

async def extract_html(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        user_agent = random.choice(USER_AGENTS)
        context = await browser.new_context(user_agent=user_agent)
        try:
            page = await context.new_page()

            await asyncio.sleep(random.uniform(1.5, 4.0))  # Delay before navigating

            await page.goto(url, timeout=60000)

            await asyncio.sleep(random.uniform(2.0, 4.0))  # Let page settle

            await simulate_human_behavior(page)

            await asyncio.sleep(random.uniform(1.0, 2.0))  # Additional wait after scroll

            html = await page.content()
            return html

        except Exception as e:
            print(f"[ERROR] Failed to extract HTML: {e}")
            return ""

        finally:
            await context.close()
            await browser.close()