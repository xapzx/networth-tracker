from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from networth_tracker.forms import CustomUserChangeForm, CustomUserCreationForm
from networth_tracker.models import (
    Account,
    BankAccount,
    CustomUser,
    Etf,
    EtfTransaction,
    Superannuation,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    ordering = ["-created_at"]
    list_display = [
        "email",
        "pk",
        "is_verified",
        "created_at",
        "last_login",
        "is_staff",
        "is_active",
    ]
    list_filter = ["is_verified", "is_staff"]
    filter_horizontal = ["groups", "user_permissions"]
    readonly_fields = [
        "created_at",
        "updated_at",
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
        ("Dates", {"fields": ("created_at", "updated_at", "last_login")}),
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
    readonly_fields = [
        "created_at",
        "updated_at",
    ]

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
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ["user", "bank", "account_name", "balance", "interest_rate"]

    search_fields = ["bank", "account_name", "user__email"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "User Details",
            {"fields": ("user",)},
        ),
        (
            "Bank Account Details",
            {
                "fields": (
                    "bank",
                    "account_name",
                    "balance",
                    "interest_rate",
                )
            },
        ),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Etf)
class EtfAdmin(admin.ModelAdmin):
    list_display = ["user", "ticker", "fund_name", "units_held", "average_cost"]

    search_fields = ["ticker", "fund_name", "user__email"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "User Details",
            {"fields": ("user",)},
        ),
        (
            "Etf Details",
            {
                "fields": (
                    "ticker",
                    "fund_name",
                    "units_held",
                    "average_cost",
                )
            },
        ),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(EtfTransaction)
class EtfTransactionAdmin(admin.ModelAdmin):
    list_display = ["etf", "transaction_type", "units", "order_cost"]
    list_filter = ["transaction_type"]
    search_fields = ["etf__ticker", "etf__fund_name", "etf__user__email"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "Etf Details",
            {"fields": ("etf",)},
        ),
        (
            "Transaction Details",
            {
                "fields": (
                    "transaction_type",
                    "order_date",
                    "units",
                    "order_cost",
                    "brokerage",
                )
            },
        ),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Superannuation)
class SuperannuationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "provider",
        "investment_plan",
        "balance",
        "market_returns",
        "voluntary_contributions",
    ]

    search_fields = ["provider", "user__email"]
    readonly_fields = [
        "created_at",
        "updated_at",
    ]

    fieldsets = (
        (
            "User Details",
            {"fields": ("user",)},
        ),
        (
            "Superannuation Details",
            {
                "fields": (
                    "provider",
                    "investment_plan",
                    "balance",
                    "market_returns",
                    "voluntary_contributions",
                )
            },
        ),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
