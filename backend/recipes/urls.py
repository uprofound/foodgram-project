from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeSpecialView, RecipeViewSet,
                    TagViewSet)

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        RecipeSpecialView.as_view(),
        name='shopping_cart'
    ),
    path(
        'recipes/<int:recipe_id>/favorite/',
        RecipeSpecialView.as_view(),
        name='favorite'
    ),
    path('', include(router.urls)),
]
