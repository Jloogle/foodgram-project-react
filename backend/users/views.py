from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.http import Http404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ListSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet, TokenCreateView

from .models import CustomUser, Follow
from .serializers import CustomUserSerializer, SubscriptionSerializer


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny, )

    def get_subscribe_serializer(self, *args, **kwargs):
        kwargs.setdefault('context', self.get_serializer_context())
        return SubscriptionSerializer(*args, **kwargs)

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        following_list = CustomUser.objects.filter(following__user=request.user)
        paginator = PageNumberPagination()
        paginator.page_size_query_param = 'limit'
        authors = paginator.paginate_queryset(following_list, request=request)
        serializer = ListSerializer(
            child=SubscriptionSerializer(),
            context=self.get_serializer_context()
        )
        return paginator.get_paginated_response(
            serializer.to_representation(authors)
        )

    def create_subscribe(self, request, author):
        user = request.user
        if user == author:
            return Response(
                    {'ERROR': 'Вы не можете подписаться на самого себя!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        try:
            subscribe = Follow.objects.create(author=author, user=user)
            serializer = self.get_subscribe_serializer(subscribe.author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response(
                {'ERROR': 'Вы не можете подписаться дважды!'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete_subscribe(self, request, author):
        user = request.user
        try:
            Follow.objects.get(author=author, user=user).delete()
        except Follow.DoesNotExist:
            return Response(
                {'ERROR': 'Несуществующая подписка не может быть отменена'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {'detail': f'Подписка на {author} отменена!'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,),
        serializer_class=SubscriptionSerializer
    )
    def subscribe(self, request, id=None):
        try:
            author = get_object_or_404(CustomUser, id=id)
        except Http404:
            return Response(
                {'ERROR': 'Страница автора не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        if request.method == 'POST':
            return self.create_subscribe(request, author)
        return self.delete_subscribe(request, author)


class CheckBlockAndTokenCreate(TokenCreateView):
    def _action(self, serializer):
        if serializer.user.is_block:
            return Response(
                {'ERROR': 'Данный пользователь заблокирован!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super()._action(serializer)
