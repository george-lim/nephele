import pytest
from src.core.sync_playwright import Playwright


# NOTE: Code inside `with sync_playwright():` cannot be seen by Coverage.py.
#       Playwright's `sync_playwright()` executes code in another process.
def test_execute():
    playwright = Playwright("telegram_000000000")
    playwright.execute(lambda *args, **kwargs: None)


def test_execute_exception():
    def bot(*args, **kwargs):
        raise Exception("bot failed")

    with pytest.raises(Exception) as exception_info:
        playwright = Playwright("telegram_000000000")
        playwright.execute(bot)

    assert str(exception_info.value) == "bot failed"
