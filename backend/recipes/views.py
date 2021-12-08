from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
