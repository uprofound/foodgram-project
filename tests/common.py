def api_create_user(client, prefix=None):
    from django.contrib.auth import get_user_model

    username = f'{prefix}_test_username' if prefix else 'test_username'
    data = {
        'username': username,
        'email': f'{username}@fake.ru',
        'first_name': 'test_first_name',
        'last_name': 'test_last_name',
        'password': 'test_password'
    }
    client.post('/api/users/', data=data)

    return get_user_model().objects.get(username=data['username'])


def auth_client(user):
    from rest_framework.authtoken.models import Token
    from rest_framework.test import APIClient

    token = Token.objects.create(user=user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {str(token)}')

    return client
