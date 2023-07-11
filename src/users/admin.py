from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ["groups", "user_permissions", "password"]
    readonly_fields = [
        "last_login",
        "is_superuser",
        "is_staff",
        "is_active",
        "email",
    ]
    list_filter = ["is_active", "role"]
    list_display = ["email", "first_name", "last_name", "role", "is_active"]
    search_fields = ["email", "first_name", "last_name", "role", "is_active"]