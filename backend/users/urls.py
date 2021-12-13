from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, SubscriptionListView, SubscriptionView

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')


urlpatterns = [
    path(
        'users/subscriptions/',
        SubscriptionListView.as_view(),
        name='subsriptions'
    ),
    path(
        'users/<int:user_id>/subscribe/',
        SubscriptionView.as_view(),
        name='subscribe'
    ),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
    path('', include(router.urls)),
]
