from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                     ShoppingCart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    list_filter = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'favorite_count')
    list_filter = ('name', 'author', 'tags')
    inlines = (RecipeIngredientInline, )

    def favorite_count(self, obj):
        return Favorite.objects.filter(recipe=obj).count()


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
