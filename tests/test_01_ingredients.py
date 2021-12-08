import pytest

from .common import api_create_user, auth_client


class Test01IngredientAPI:
    BASE_URL = '/api/ingredients/'

    @pytest.mark.django_db(transaction=True)
    def test_01_get_ingredient_list_not_authorized(self, client):
        response = client.get(self.BASE_URL)
        assert response.status_code != 404, (
            f'Страница "{self.BASE_URL}" не найдена, '
            'проверьте этот адрес в urls.py'
        )
        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе к "{self.BASE_URL}" '
            'без токена авторизации возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_post_ingredient_not_allowed(self, client):
        data = {}
        response = client.post(self.BASE_URL, data=data)
        assert response.status_code in (401, 405), (
            'Проверьте, что создание ингредиента недоступно '
            f'через неавторизованный POST запрос к "{self.BASE_URL}"'
        )

        _user = api_create_user(client)
        _auth_client = auth_client(_user)
        response = _auth_client.post(self.BASE_URL, data=data)

        assert response.status_code == 405, (
            'Проверьте, что создание ингредиента недоступно '
            f'через авторизованный POST запрос к "{self.BASE_URL}"'
        )
