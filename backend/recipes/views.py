from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import DestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .models import Ingredient, Recipe, ShoppingCart, Tag
from .permissions import IsAuthor, IsReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)
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

    @action(methods=['get'], detail=False,
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        return get_shopping_list_pdf(request.user.id)


class ShoppingCartView(RetrieveAPIView, DestroyAPIView):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, recipe_id, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        _, created = ShoppingCart.objects.get_or_create(
            recipe=recipe,
            user=request.user
        )
        if not created:
            return Response(
                {'Ошибка добавления в список покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serialized = ShoppingCartSerializer(recipe)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id, *args, **kwargs):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        try:
            obj = ShoppingCart.objects.get(recipe=recipe, user=request.user)
            obj.delete()
            return Response(
                {'Рецепт успешно удалён из списка покупок'},
                status=status.HTTP_204_NO_CONTENT
            )
        except ShoppingCart.DoesNotExist:
            return Response(
                {'Ошибка удаления из списка покупок'},
                status=status.HTTP_400_BAD_REQUEST
            )
