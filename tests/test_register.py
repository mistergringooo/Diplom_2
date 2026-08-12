import pytest

from data import ERROR_USER_ALREADY_EXISTS, ERROR_MISSING_REQUIRED_FIELDS
from helpers import generate_user
from api_client import StellarBurgersAPI


class TestRegister:
    def test_register_unique_user(self):
        user = generate_user()

        response = StellarBurgersAPI.register_user(user)

        assert response.status_code == 200
        body = response.json()
        assert body['success'] is True
        assert 'accessToken' in body

        StellarBurgersAPI.delete_user(body['accessToken'])

    @pytest.mark.parametrize('modify_user, expected_message', [
        (lambda user: user, ERROR_USER_ALREADY_EXISTS),
        (lambda user: {**user, 'email': ''}, ERROR_MISSING_REQUIRED_FIELDS),
    ])
    def test_register_invalid(self, modify_user, expected_message):
        user = generate_user()
        StellarBurgersAPI.register_user(user)

        invalid_user = modify_user(user)
        response = StellarBurgersAPI.register_user(invalid_user)

        assert response.status_code == 403
        assert response.json()['message'] == expected_message