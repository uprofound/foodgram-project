from django.db.models import Sum
from django.http import HttpResponse

from .models import RecipeIngredient


def get_shopping_list_pdf(user_id):
    shopping_list = RecipeIngredient.objects.filter(
        recipe__shopping_cart__user=user_id
    ).values_list('ingredient__name', 'ingredient__measurement_unit', 'amount')

    summed_ingredients = shopping_list.values(
        'ingredient__name', 'ingredient__measurement_unit'
    ).annotate(total=Sum('amount'))

    shopping_list = ['{} ({}) - {}\n'.format(
        ingredient['ingredient__name'],
        ingredient['ingredient__measurement_unit'],
        ingredient['total']
    ) for ingredient in summed_ingredients]

    response = HttpResponse(shopping_list, 'Content-Type: application/txt')
    response['Content-Disposition'] = ('attachment; '
                                       'filename="shopping_list.txt"')
    return response
