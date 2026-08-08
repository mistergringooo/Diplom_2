import uuid

import requests

BASE_URL = 'https://stellarburgers.education-services.ru/api'


def generate_user():
    return {
        'email': f'{uuid.uuid4()}@yandex.ru',
        'password': 'password123',
        'name': 'Test User'
    }


def get_ingredient_ids(count=2):
    response = requests.get(f'{BASE_URL}/ingredients')
    ingredients = response.json()['data']
    return [ingredients[i]['_id'] for i in range(count)]


class TestOrders:
    def test_create_order_with_auth(self):
        user = generate_user()
        register_response = requests.post(f'{BASE_URL}/auth/register', json=user)
        token = register_response.json()['accessToken']

        ingredient_ids = get_ingredient_ids()

        response = requests.post(
            f'{BASE_URL}/orders',
            json={'ingredients': ingredient_ids},
            headers={'Authorization': token}
        )

        assert response.status_code == 200
        assert response.json()['success'] is True

        requests.delete(f'{BASE_URL}/auth/user', headers={'Authorization': token})

    def test_create_order_without_auth(self):
        ingredient_ids = get_ingredient_ids()

        response = requests.post(
            f'{BASE_URL}/orders',
            json={'ingredients': ingredient_ids}
        )

        assert response.status_code == 200
        assert response.json()['success'] is True

    def test_create_order_without_ingredients(self):
        user = generate_user()
        register_response = requests.post(f'{BASE_URL}/auth/register', json=user)
        token = register_response.json()['accessToken']

        response = requests.post(
            f'{BASE_URL}/orders',
            json={'ingredients': []},
            headers={'Authorization': token}
        )

        assert response.status_code == 400
        assert response.json()['message'] == 'Ingredient ids must be provided'

        requests.delete(f'{BASE_URL}/auth/user', headers={'Authorization': token})

    def test_create_order_invalid_ingredient_hash(self):
        user = generate_user()
        register_response = requests.post(f'{BASE_URL}/auth/register', json=user)
        token = register_response.json()['accessToken']

        response = requests.post(
            f'{BASE_URL}/orders',
            json={'ingredients': ['invalid_hash_123']},
            headers={'Authorization': token}
        )

        assert response.status_code == 500

        requests.delete(f'{BASE_URL}/auth/user', headers={'Authorization': token})