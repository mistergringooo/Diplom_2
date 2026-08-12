from data import ERROR_NO_INGREDIENTS_PROVIDED
from api_client import StellarBurgersAPI


class TestOrders:
    def test_create_order_with_auth(self, registered_user):
        _, register_body = registered_user
        token = register_body['accessToken']

        ingredients_response = StellarBurgersAPI.get_ingredients()
        ingredient_ids = [ingredients_response.json()['data'][i]['_id'] for i in range(2)]

        response = StellarBurgersAPI.create_order(ingredient_ids, token=token)

        assert response.status_code == 200
        assert response.json()['success'] is True

    def test_create_order_without_auth(self):
        ingredients_response = StellarBurgersAPI.get_ingredients()
        ingredient_ids = [ingredients_response.json()['data'][i]['_id'] for i in range(2)]

        response = StellarBurgersAPI.create_order(ingredient_ids)

        assert response.status_code == 200
        assert response.json()['success'] is True

    def test_create_order_without_ingredients(self, registered_user):
        _, register_body = registered_user
        token = register_body['accessToken']

        response = StellarBurgersAPI.create_order([], token=token)

        assert response.status_code == 400
        assert response.json()['message'] == ERROR_NO_INGREDIENTS_PROVIDED

    def test_create_order_invalid_ingredient_hash(self, registered_user):
        _, register_body = registered_user
        token = register_body['accessToken']

        response = StellarBurgersAPI.create_order(['invalid_hash_123'], token=token)

        assert response.status_code == 500