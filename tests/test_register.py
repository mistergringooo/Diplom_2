import uuid

import pytest
import requests

BASE_URL = 'https://stellarburgers.education-services.ru/api'


def generate_user():
    return {
        'email': f'{uuid.uuid4()}@yandex.ru',
        'password': 'password123',
        'name': 'Test User'
    }


class TestRegister:
    def test_register_unique_user(self):
        user = generate_user()

        response = requests.post(f'{BASE_URL}/auth/register', json=user)

        assert response.status_code == 200
        body = response.json()
        assert body['success'] is True
        assert 'accessToken' in body

        token = body['accessToken']
        requests.delete(f'{BASE_URL}/auth/user', headers={'Authorization': token})

    @pytest.mark.parametrize('modify_user, expected_message', [
        (lambda user: user, 'User already exists'),
        (lambda user: {**user, 'email': ''}, 'Email, password and name are required fields'),
    ])
    def test_register_invalid(self, modify_user, expected_message):
        user = generate_user()
        requests.post(f'{BASE_URL}/auth/register', json=user)

        invalid_user = modify_user(user)
        response = requests.post(f'{BASE_URL}/auth/register', json=invalid_user)

        assert response.status_code == 403
        assert response.json()['message'] == expected_message