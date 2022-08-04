from django_filters import rest_framework as filters

from .models import Ingredient, Recipe


class IngredientSearchFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='get_is_favorited',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='get_is_in_shopping_cart',
    )

    def get_is_favorited(self, queryset, name, value):
        recipes = Recipe.objects.filter(favorites__user=self.request.user)
        return recipes

    def get_is_in_shopping_cart(self, queryset, name, value):
        recipes = Recipe.objects.filter(shopping_cart__user=self.request.user)
        return recipes

    class Meta:
        model = Recipe
        fields = ('author',)
