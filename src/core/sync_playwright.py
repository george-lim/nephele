import os
from pathlib import Path
from time import strftime

from playwright.sync_api import sync_playwright


class Playwright:
    def __init__(self, user_id):
        self.default_timeout_ms = 10000
        self.firefox_binary_path_str = os.environ.get("FIREFOX_BINARY_PATH")

        self._screenshot_path = Path(
            f"/tmp/playwright_{user_id}_{strftime('%Y%m%dT%H%M%S')}.png"
        )

    @property
    def screenshot_path(self):
        return self._screenshot_path

    def execute(self, bot):
        with sync_playwright() as playwright:
            browser = None
            page = None

            try:
                browser = playwright.firefox.launch(self.firefox_binary_path_str)
                page = browser.new_page()

                page.set_default_timeout(self.default_timeout_ms)
                response = bot(page)

                browser.close()
                return response
            except Exception:
                if page is not None:
                    page.screenshot(path=self.screenshot_path)

                if browser is not None:
                    browser.close()

                raise
