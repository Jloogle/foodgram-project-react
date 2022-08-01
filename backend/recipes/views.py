import csv

from django.http.response import FileResponse
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Tag, Recipe, Favorite, Ingredient, ShoppingCart, RecipeIngredient
from .serializers import TagSerializer, IngredientSerializer, RecipeGetSerializer, RecipeCreateSerializer, FavoriteSerializer, ShoppingCartSerializer
from .permissions import AuthorOrReadOnly, AdminOrReadOnly
from .filters import IngredientSearchFilter, RecipeFilter
from foodgram.pagination import LimitPageNumberPaginator


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    permission_classes = (AdminOrReadOnly,)
    pagination_class = None
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientSearchFilter


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnly,)
    default_serializer_class = RecipeCreateSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = LimitPageNumberPaginator

    def get_serializer_class(self):
        if self.request.method in ('GET',):
            return RecipeGetSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            recipe_favorite, create = Favorite.objects.get_or_create(
                user=user, recipe=recipe
            )
            if create:
                serializer = FavoriteSerializer()
                return Response(
                    serializer.to_representation(instance=recipe_favorite),
                    status=status.HTTP_201_CREATED
                )
        if request.method == 'DELETE':
            Favorite.objects.filter(recipe=recipe, user=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk)
        if request.method == 'POST':
            recipe_cart, create = ShoppingCart.objects.get_or_create(
                user=user,
                recipe=recipe)
            if create:
                serializer = ShoppingCartSerializer()
                return Response(
                    serializer.to_representation(instance=recipe_cart),
                    status=status.HTTP_201_CREATED
                )
        if request.method == 'DELETE':
            ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'],
            detail=False,
            permission_classes=(IsAuthenticated,)
            )
    def download_shopping_cart(self, request):
        user = request.user
        recipes = user.recipes.all()
        shopping_cart = {}
        for recipe in recipes:
            ingredients = RecipeIngredient.objects.filter(
                recipe=recipe
            ).all()
            for ingredient in ingredients:
                name = ingredient.ingredient.name
                amount = ingredient.amount
                if name not in shopping_cart.keys():
                    shopping_cart[name] = amount
                else:
                    shopping_cart[name] += amount
        with open('shopping_cart.txt', 'w+', encoding='utf-8') as file:
            for ingredient, amount in shopping_cart.items():
                measurement_unit = get_object_or_404(
                    Ingredient, name=ingredient
                ).measurement_unit
                file.write(f'{ingredient} - {amount}  {measurement_unit}\n')
        file = open('shopping_cart.txt', 'rb')
        response = FileResponse(file, content_type='text/plain')
        return response
