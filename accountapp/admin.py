from django.contrib import admin
from accountapp.models import User, Profile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass