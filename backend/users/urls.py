from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
]
