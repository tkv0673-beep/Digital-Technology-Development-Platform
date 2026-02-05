"""
Admin configuration for tokens service
"""
from django.contrib import admin
from .models import User, RefreshToken, PasswordResetToken


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'created_at')
    list_filter = ('role', 'created_at')
    search_fields = ('username', 'email')


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'is_revoked', 'expires_at', 'created_at')
    list_filter = ('is_revoked', 'created_at')
    search_fields = ('user__username', 'token')


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_used', 'expires_at', 'created_at')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'token')

