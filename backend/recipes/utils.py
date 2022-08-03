from rest_framework import exceptions

from .models import RecipeIngredient


def double_checker(item_list):
    """Проверяет элементы на повтор"""
    for item in item_list:
        if len(item) == 0:
            raise exceptions.ValidationError(
                f'{item} должен иметь хотя бы одну позицию!'
            )
        for element in item:
            if item.count(element) > 1:
                raise exceptions.ValidationError(
                    f'{element} уже есть в рецепте!'
                )


def create_ingredients(ingredients, recipe):
    ingredient_list = []
    for ingredient in ingredients:
        ingredient_id = ingredient['id']
        amount = ingredient['amount']
        recipe_ingredient = RecipeIngredient(
            recipe=recipe,
            ingredient=ingredient_id,
            amount=amount
        )
        ingredient_list.append(recipe_ingredient)
    RecipeIngredient.objects.bulk_create(ingredient_list)
