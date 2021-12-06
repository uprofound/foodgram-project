import pytest


class Test01IngredientAPI:
    BASE_URL = '/api/ingredients/'

    @pytest.mark.django_db(transaction=True)
    def test_01_ingredients_not_auth(self, client):
        response = client.get(self.BASE_URL)
        assert response.status_code != 404, (
            f'Страница `{self.BASE_URL}` не найдена, '
            'проверьте этот адрес в urls.py'
        )
        assert response.status_code == 200, (
            f'Проверьте, что при GET запросе к `{self.BASE_URL}` '
            'без токена авторизации возвращается статус 200'
        )

    @pytest.mark.django_db(transaction=True)
    def test_02_ingredient_post_not_allowed(self, client):
        data = {}
        response = client.post(self.BASE_URL, data=data)
        assert response.status_code == 405, (
            'Проверьте, что создание ингредиента недоступно '
            f'через POST запрос к `{self.BASE_URL}`'
        )
