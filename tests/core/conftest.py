import os

import pytest


@pytest.fixture(autouse=True)
def add_service_name(monkeypatch):
    monkeypatch.setitem(os.environ, "SERVICE_NAME", "core")
