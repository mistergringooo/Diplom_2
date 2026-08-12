import uuid


def generate_user():
    return {
        'email': f'{uuid.uuid4()}@yandex.ru',
        'password': 'password123',
        'name': 'Test User'
    }