import requests

from data import BASE_URL


class StellarBurgersAPI:
    @staticmethod
    def register_user(user):
        return requests.post(f'{BASE_URL}/auth/register', json=user)

    @staticmethod
    def delete_user(token):
        return requests.delete(f'{BASE_URL}/auth/user', headers={'Authorization': token})

    @staticmethod
    def login_user(email, password):
        return requests.post(f'{BASE_URL}/auth/login', json={'email': email, 'password': password})

    @staticmethod
    def get_ingredients():
        return requests.get(f'{BASE_URL}/ingredients')

    @staticmethod
    def create_order(ingredient_ids, token=None):
        headers = {'Authorization': token} if token else {}
        return requests.post(f'{BASE_URL}/orders', json={'ingredients': ingredient_ids}, headers=headers)