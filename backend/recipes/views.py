from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import LimitPageNumberPagination
from .permissions import IsAuthor, IsReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeSpecialSerializer, TagSerializer)
from .utils import get_shopping_list_pdf


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthor | IsReadOnly,)
    pagination_class = LimitPageNumberPagination

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        return get_shopping_list_pdf(request.user.id)


class RecipeSpecialView(RetrieveAPIView, DestroyAPIView):
    MODELS = {
        'shopping_cart': ShoppingCart,
        'favorite': Favorite,
    }
    WORD_CASES = {
        'shopping_cart': ['список покупок', 'списка покупок'],
        'favorite': ['избранное', 'избранного'],
    }
    serializer_class = RecipeSpecialSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, recipe_id, *args, **kwargs):
        url_name = self.request.resolver_match.url_name
        model = self.MODELS[url_name]
        recipe = get_object_or_404(Recipe, id=recipe_id)
        _, created = model.objects.get_or_create(
            recipe=recipe,
            user=request.user
        )
        if not created:
            return Response(
                {f'Ошибка добавления в {self.WORD_CASES[url_name][0]}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serialized = RecipeSpecialSerializer(recipe)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id, *args, **kwargs):
        url_name = self.request.resolver_match.url_name
        model = self.MODELS[url_name]
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            obj = model.objects.get(recipe=recipe, user=request.user)
            obj.delete()
            return Response(
                {f'Рецепт успешно удалён из {self.WORD_CASES[url_name][1]}'},
                status=status.HTTP_204_NO_CONTENT
            )
        except model.DoesNotExist:
            return Response(
                {f'Ошибка удаления из {self.WORD_CASES[url_name][1]}'},
                status=status.HTTP_400_BAD_REQUEST
            )
