from django.urls import include, path
from rest_framework import routers
from djoser.views import TokenDestroyView

from .views import CustomUserViewSet, CheckBlockAndTokenCreate

router = routers.SimpleRouter()
router.register(r'users', CustomUserViewSet, basename='users')

app_name = 'users'

urlpatterns = [
    path('auth/token/login/', CheckBlockAndTokenCreate.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
    path('', include(router.urls))
]
