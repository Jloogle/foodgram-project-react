from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ListSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.views import UserViewSet

from .models import CustomUser, Follow
from .serializers import CustomUserSerializer, SubscriptionSerializer


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (AllowAny, )

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

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(CustomUser, id=id)

        if request.method == 'POST':
            subscribe = Follow.objects.filter(
                author=author, user=user).exists()
            if subscribe:
                Response(status=status.HTTP_400_BAD_REQUEST)
            Follow.objects.get_or_create(user=user, author=author)
            serializer = SubscriptionSerializer(
                context=self.get_serializer_context()
            )
            return Response(
                serializer.to_representation(instance=author),
                status=status.HTTP_201_CREATED
            )
        if request.method == 'DELETE':
            Follow.objects.filter(author=author, user=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
