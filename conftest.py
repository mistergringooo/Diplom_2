import pytest

from helpers import generate_user
from api_client import StellarBurgersAPI


@pytest.fixture
def registered_user():
    user = generate_user()
    response = StellarBurgersAPI.register_user(user)
    body = response.json()

    yield user, body

    StellarBurgersAPI.delete_user(body['accessToken'])