import copy

import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture
def test_client():
    """Create a reusable FastAPI test client and restore app state after each test."""
    original_activities = copy.deepcopy(app_module.activities)

    with TestClient(app_module.app) as client:
        yield client

    app_module.activities = copy.deepcopy(original_activities)
