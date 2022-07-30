from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from users.mixins import SubscribeMixin
from users.models import CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'email', 'id', 'username', 'password',  'first_name', 'last_name'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }


class CustomUserSerializer(UserSerializer, SubscribeMixin):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'id',
                  'last_name', 'email', 'is_subscribed', )
