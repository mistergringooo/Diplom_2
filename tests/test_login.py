from data import ERROR_INVALID_CREDENTIALS
from api_client import StellarBurgersAPI


class TestLogin:
    def test_login_existing_user(self, registered_user):
        user, _ = registered_user

        response = StellarBurgersAPI.login_user(user['email'], user['password'])

        assert response.status_code == 200
        assert response.json()['success'] is True

    def test_login_invalid_credentials(self):
        response = StellarBurgersAPI.login_user('nonexistent@yandex.ru', 'wrongpassword')

        assert response.status_code == 401
        assert response.json()['message'] == ERROR_INVALID_CREDENTIALS