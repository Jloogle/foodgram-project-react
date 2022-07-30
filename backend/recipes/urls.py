from django.urls import path, include
from rest_framework import routers

from .views import RecipeViewSet, TagViewSet, IngredientViewSet

router = routers.SimpleRouter()
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

app_name = 'recipes'

urlpatterns = [
    path('', include(router.urls))
]
