from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

class UserProfileAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'date_of_birth', 'profile_picture')

admin.site.register(UserProfile, UserProfileAdmin)