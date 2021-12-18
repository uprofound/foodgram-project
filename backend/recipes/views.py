from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
# from rest_framework.filters import SearchFilter
from rest_framework.generics import RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .filters import RecipeFilter
from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .pagination import LimitPageNumberPagination
from .permissions import IsAuthor, IsReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          RecipeSpecialSerializer, TagSerializer)
from .utils import get_shopping_list


class IngredientViewSet(ReadOnlyModelViewSet):
    # queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    # filter_backends = (SearchFilter,)  # не понимаю - почему не срабатывает?
    # search_fields = ('^name',)         # сделала поиск через get_queryset

    def get_queryset(self):
        name_starts_with = self.request.query_params.get('name')
        if name_starts_with:
            return Ingredient.objects.filter(name__startswith=name_starts_with)
        return Ingredient.objects.all()


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthor | IsReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter
    pagination_class = LimitPageNumberPagination

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        return get_shopping_list(request.user.id)


class RecipeSpecialView(RetrieveDestroyAPIView):
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

    def initiate(self, url_name):
        model = self.MODELS[url_name]
        recipe_id = self.kwargs.get('recipe_id')
        recipe = get_object_or_404(Recipe, id=recipe_id)
        return model, recipe

    def get(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name
        model, recipe = self.initiate(url_name)
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

    def delete(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name
        model, recipe = self.initiate(url_name)
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
