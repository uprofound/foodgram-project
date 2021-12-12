from djoser.views import UserViewSet

from .models import User
from .pagination import LimitPageNumberPagination
from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitPageNumberPagination
