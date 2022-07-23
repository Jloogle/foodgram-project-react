from django.urls import include, path
from rest_framework import routers

from .views import CustomUserViewSet

router = routers.SimpleRouter()
router.register(r'users', CustomUserViewSet, basename='users')

app_name = 'users'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]
