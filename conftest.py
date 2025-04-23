import pytest

BASE_URL = 'http://localhost:8065/api/v4'


@pytest.fixture()
def base_url():
    return BASE_URL