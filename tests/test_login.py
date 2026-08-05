import uuid

import requests

BASE_URL = 'https://stellarburgers.education-services.ru/api'


def generate_user():
    return {
        'email': f'{uuid.uuid4()}@yandex.ru',
        'password': 'password123',
        'name': 'Test User'
    }


def register_user(user):
    response = requests.post(f'{BASE_URL}/auth/register', json=user)
    return response.json()


def test_login_existing_user():
    user = generate_user()
    register_data = register_user(user)

    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': user['email'],
        'password': user['password']
    })

    assert response.status_code == 200
    assert response.json()['success'] is True

    # уборка
    token = register_data['accessToken']
    requests.delete(f'{BASE_URL}/auth/user', headers={'Authorization': token})


def test_login_invalid_credentials():
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'email': 'nonexistent@yandex.ru',
        'password': 'wrongpassword'
    })

    assert response.status_code == 401
    assert response.json()['message'] == 'email or password are incorrect'