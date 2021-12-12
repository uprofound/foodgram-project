import random

from django.core.management.base import BaseCommand
from django.db import transaction

from recipes.models import (Ingredient, Recipe, RecipeIngredient,  # isort:skip
                            Tag)
from users.models import User  # isort:skip


class Command(BaseCommand):
    @staticmethod
    def add_user(num):
        return User.objects.create(
            first_name=f'Алиса{num}',
            last_name=f'Селезнёва{num}',
            username=f'alice{num}',
            email=f'alice{num}@fake.ru',
            password=('pbkdf2_sha256$180000$PY9vg4EkpTak$Eu11r'
                      'p13/pryvHo7WMZ95t/7ESNX3E8WgeLLkmz7UH4=')  # _Qwerty123_
        )

    @staticmethod
    def add_ingredients():
        _ingredient = Ingredient.objects.create(
            name='мангустин',
            measurement_unit='штука'
        )
        _ingredients_id = [_ingredient.id]
        _ingredient = Ingredient.objects.create(
            name='петеяровое масло',
            measurement_unit='столовая ложка'
        )
        _ingredients_id.append(_ingredient.id)
        return _ingredients_id

    @staticmethod
    def add_tags():
        names = ['завтрак', 'обед', 'ужин']
        colors = ['#008000', '#ff0000', '#8b00ff']
        slugs = ['breakfast', 'lunch', 'dinner']
        _tags_id = []
        for _tag in list(zip(names, colors, slugs)):
            _tags_id.append(
                Tag.objects.create(
                    name=_tag[0],
                    color=_tag[1],
                    slug=_tag[2]
                ).id
            )
        return _tags_id

    @staticmethod
    def add_recipe(author_id, ingredients_id, tags_id):
        recipe = Recipe.objects.create(
            author=author_id,
            name='Брамбулет',
            image='recipes/images/brambulet.png',
            text=('Берешь обыкновенный мангустин и жаришь его '
                  'на петеяровом масле минут пять.'),
            cooking_time=5
        )
        ingredients = [
            {'id': ingredients_id[0], 'amount': 1},
            {'id': ingredients_id[1], 'amount': 1}
        ]
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )
        recipe.tags.set([random.choice(tags_id)])

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            # добавляем два ингредиента с предустановленными атрибутами
            ingredients_id = self.add_ingredients()

            # добавляем три тега с предустановленными атрибутами
            tags_id = self.add_tags()

            # добавляем 15 пользователей с предустановленными атрибутами
            # с одинаковыми рецептами и разными тегами
            users = [self.add_user(num) for num in range(1, 16)]
            for user in users:
                self.add_recipe(user, ingredients_id, tags_id)
