from django_filters import rest_framework as filters

from .models import Ingredient, Recipe, Tag
from users.models import CustomUser


class IngredientSearchFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    author = filters.ModelChoiceFilter(queryset=CustomUser.objects.all())
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
        fields = ('tags', 'author')

