import pytest

from .common import api_create_user, auth_client


class Test02UserAPI:
    BASE_URL = '/api/users/'
    USER_RESPONSE_FIELDS = (
        'email',
        'id',
        'username',
        'first_name',
        'last_name'
    )

    @pytest.mark.django_db(transaction=True)
    def test_01_get_user_list_not_authorized(self, client):
        response = client.get(self.BASE_URL)

        assert response.status_code != 404, (
            f'Страница "{self.BASE_URL}" не найдена,'
            ' проверьте этот адрес в urls.py'
        )

        assert response.status_code == 200, (
            f'Проверьте, что GET запрос к "{self.BASE_URL}"'
            ' не требует авторизации'
        )

        _user = api_create_user(client)
        response = client.get(self.BASE_URL)
        data = response.json()

        assert data[0]['email'] == _user.email, (
            f'Проверьте, что GET запрос к "{self.BASE_URL}"'
            ' возвращает корректные данные'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_get_user_me_authorized(self, client):
        url = f'{self.BASE_URL}me/'
        response = client.get(url)

        assert response.status_code != 404, (
            f'Страница "{url}" не найдена, проверьте этот адрес в urls.py'
        )

        assert response.status_code == 401, (
            f'Проверьте, что GET запрос к "{url}" требует авторизации'
        )

        _user = api_create_user(client)
        _auth_client = auth_client(_user)
        response = _auth_client.get(url)

        assert response.status_code == 200, (
            f'Проверьте, что авторизованный GET запрос к "{url}"'
            ' возвращает статус 200'
        )

        data = response.json()
        _data = {}
        for field in self.USER_RESPONSE_FIELDS:
            _data[field] = getattr(_user, field)

        assert data == _data, (
            f'Проверьте, что авторизованный GET запрос к "{self.BASE_URL}"'
            ' возвращает корректные данные'
        )

    @pytest.mark.django_db(transaction=True)
    def test_03_get_user_authorized(self, client):
        _first_user = api_create_user(client, prefix='first')
        url = f'{self.BASE_URL}{str(_first_user.id)}/'
        response = client.get(url)

        assert response.status_code != 404, (
            f'Страница "{url}" не найдена, проверьте этот адрес в urls.py'
        )

        assert response.status_code == 401, (
            f'Проверьте, что GET запрос к "{url}" требует авторизации'
        )

        _auth_client = auth_client(_first_user)
        _second_user = api_create_user(client, prefix='second')
        url = f'{self.BASE_URL}{str(_second_user.id)}/'
        response = _auth_client.get(url)

        assert response.status_code == 200, (
            'Проверьте, что авторизованному пользователю доступен '
            'просмотр профилей других пользователей'
        )

        data = response.json()
        _data = {}
        for field in self.USER_RESPONSE_FIELDS:
            _data[field] = getattr(_second_user, field)

        assert data == _data, (
            f'Проверьте, что авторизованный GET запрос к "{self.BASE_URL}"'
            ' возвращает корректные данные'
        )
