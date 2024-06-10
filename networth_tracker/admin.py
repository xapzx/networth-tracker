from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ["-date_joined"]
    list_display = [
        "email",
        "pk",
        "is_verified",
        "date_joined",
        "last_login",
        "is_staff",
        "is_active",
    ]
    list_filter = ["is_verified", "is_staff"]
    filter_horizontal = ["groups", "user_permissions"]
    readonly_fields = [
        "date_joined",
        "last_login",
    ]

    fieldsets = (
        (
            None,
            {"fields": ("email", "password", "is_verified")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("date_joined", "last_login")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )

    search_fields = ("email",)
