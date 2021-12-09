from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientInline, )


admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredient)
