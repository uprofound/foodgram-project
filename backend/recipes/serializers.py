from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import (ModelSerializer, ReadOnlyField,
                                        SerializerMethodField, ValidationError)

from .models import (Favorite, Ingredient, Recipe,  # isort:skip
                     RecipeIngredient, ShoppingCart, Tag)
from users.serializers import CustomUserSerializer  # isort:skip


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class RecipeIngredientSerializer(ModelSerializer):
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(source='ingredient.measurement_unit')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        source='recipe_ingredients',
        read_only=True,
        many=True,
    )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=recipe).exists()

    def get_is_in_shopping_cart(self, recipe):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=recipe).exists()

    def validate_tags(self, data):
        if not data:
            raise ValidationError(
                'В рецепте должен быть хотя бы один тег'
            )

        if len(data) != len(set(data)):
            raise ValidationError('Теги в рецепте должны быть уникальными')

        for _id in data:
            if not Tag.objects.filter(id=_id).exists():
                raise ValidationError(f'Тег с id = {_id} не найден')

        return data

    def validate_ingredients(self, data):
        if not data:
            raise ValidationError(
                'В рецепте должен быть хотя бы один ингредиент'
            )

        ids = [item['id'] for item in data]
        if len(ids) != len(set(ids)):
            raise ValidationError(
                'Ингредиенты в рецепте должны быть уникальными'
            )
        for _id in ids:
            if not Ingredient.objects.filter(id=_id).exists():
                raise ValidationError(
                    f'Ингредиент с id = {_id} не найден'
                )

        amounts = [item['amount'] for item in data]
        for amount in amounts:
            if int(amount) <= 0:
                raise ValidationError(
                    'Количество ингредиента - целое число не менее 1'
                )

        return data

    def validate(self, data):
        data['ingredients'] = self.validate_ingredients(
            self.initial_data.get('ingredients')
        )

        data['tags'] = self.validate_tags(
            self.initial_data.get('tags')
        )

        author = self.context.get('request').user
        if self.context.get('request').method == 'POST':
            name = data.get('name')
            if Recipe.objects.filter(author=author, name=name).exists():
                raise ValidationError(
                    'У вас уже есть рецепт с таким названием'
                )
        data['author'] = author

        cooking_time = data.get('cooking_time')
        if not isinstance(cooking_time, int) or cooking_time <= 0:
            raise ValidationError(
                'Время приготовления - целое число не менее 1'
            )

        return data

    def create_recipe_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        with transaction.atomic():
            recipe = Recipe.objects.create(**validated_data)
            self.create_recipe_ingredients(ingredients, recipe)
            recipe.tags.set(tags)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        with transaction.atomic():
            recipe = super().update(recipe, validated_data)
            recipe.ingredients.clear()
            self.create_recipe_ingredients(ingredients, recipe)
            recipe.tags.set(tags)
        return recipe


class RecipeSpecialSerializer(ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
