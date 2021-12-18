from django.db.models import Sum
from django.http import HttpResponse

from .models import RecipeIngredient


def get_shopping_list(user_id):
    shopping_set = RecipeIngredient.objects.filter(
        recipe__shopping_cart__user=user_id
    ).values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(total=Sum('amount'))

    shopping_list = ['{} ({}) - {}\n'.format(
        ingredient['ingredient__name'],
        ingredient['ingredient__measurement_unit'],
        ingredient['total']
    ) for ingredient in shopping_set]

    response = HttpResponse(shopping_list, 'Content-Type: application/txt')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_list.txt"')
    return response
