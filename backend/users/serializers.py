from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .models import CustomUser, Follow
from .mixins import SubscribeMixin

User = CustomUser


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'password',  'first_name', 'last_name'
        )
        extra_kwargs = {
            'password': {'write_only': True, 'required': True},
        }


class CustomUserSerializer(UserSerializer, SubscribeMixin):

    class Meta:
        model = User
        fields = ('password', 'username', 'first_name', 'id',
                  'last_name', 'email', 'is_subscribed', )


class SubscriptionSerializer(CustomUserSerializer):
    # recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = CustomUserSerializer.Meta.fields + ('recipes_count',)

    def validate(self, data):
        author = data['following']
        user = data['follower']
        if user == author:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя!'
            )
        if Follow.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                'Вы не можете оформить подписку повторно'
            )
        return data

    def create(self, **validated_data):
        subscribe = Follow.objects.create(**validated_data)
        subscribe.save()
        return subscribe

    # def get_recipes(self):
    #     pass

    def get_recipes_count(self, obj):
        return obj.recipes.count()
