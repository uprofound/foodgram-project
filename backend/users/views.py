from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response

from .models import Subscription, User
from .pagination import LimitPageNumberPagination
from .serializers import CustomUserSerializer, SubscriptionSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination


class SubscriptionListView(ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated, )
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        return User.objects.filter(subscriptions__user=self.request.user)


class SubscriptionView(RetrieveDestroyAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        if user_id == request.user.id:
            return Response(
                {'Подписка на самого себя невозможна'},
                status=status.HTTP_400_BAD_REQUEST
            )
        if Subscription.objects.filter(
            user=request.user,
            author_id=user_id
        ).exists():
            return Response(
                {'Повторная подписка невозможна'},
                status=status.HTTP_400_BAD_REQUEST
            )

        author = get_object_or_404(User, id=user_id)
        Subscription.objects.create(
            user=request.user,
            author_id=user_id
        )
        return Response(
            self.serializer_class(author, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        get_object_or_404(User, id=user_id)
        subscription = Subscription.objects.filter(
            user=request.user,
            author_id=user_id
        )
        if subscription:
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'У вас нет подписки на указанного автора'},
            status=status.HTTP_400_BAD_REQUEST
        )
