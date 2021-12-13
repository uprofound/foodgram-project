from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Subscription, User


class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name')
    list_filter = ('email', 'username')


admin.site.register(User, CustomUserAdmin)
admin.site.register(Subscription)
