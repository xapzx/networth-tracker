from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Account, BankAccount, CustomUser


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


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    model = BankAccount
    list_display = ["pk", "first_name", "last_name", "user"]
    list_filter = [
        "allocation_intensity",
    ]
    search_fields = ("first_name", "last_name", "user__email")

    fieldsets = (
        (
            "User Details",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "date_of_birth",
                )
            },
        ),
        (
            "Finance",
            {
                "fields": (
                    "salary",
                    "eoy_cash_goal",
                    "emergency_fund",
                )
            },
        ),
        (
            "Asset Allocation",
            {
                "fields": (
                    "allocation_intensity",
                    "allocation_etfs",
                    "allocation_stocks",
                    "allocation_cryptocurrency",
                    "allocation_cash",
                    "allocation_managed_funds",
                    "allocation_other",
                )
            },
        ),
        (
            "Tax Information",
            {
                "fields": (
                    "short_term_tax_rate",
                    "long_term_tax_rate",
                )
            },
        ),
    )


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ["user", "bank", "account_name", "balance", "interest_rate"]
