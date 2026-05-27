from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


INITIAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES))
    yield
    activities.clear()
    activities.update(deepcopy(INITIAL_ACTIVITIES))