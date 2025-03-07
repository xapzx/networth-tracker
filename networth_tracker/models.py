# networth_tracker/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]


class Timestamp(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        abstract = True


class CustomUser(AbstractBaseUser, PermissionsMixin, Timestamp):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Specifies whether the user can log into the Django admin site"),
    )
    is_active = models.BooleanField(_("active status"), default=True)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email


class Account(Timestamp):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    date_of_birth = models.DateField()

    salary = models.FloatField()
    eoy_cash_goal = models.FloatField()
    emergency_fund = models.FloatField()

    CHOICES = ((0, "Light"), (1, "Normal"), (2, "Aggressive"))
    allocation_intensity = models.PositiveSmallIntegerField(choices=CHOICES, default=1)
    allocation_etfs = models.FloatField(validators=PERCENTAGE_VALIDATOR)
    allocation_stocks = models.FloatField(validators=PERCENTAGE_VALIDATOR)
    allocation_cryptocurrency = models.FloatField(validators=PERCENTAGE_VALIDATOR)
    allocation_cash = models.FloatField(validators=PERCENTAGE_VALIDATOR)
    allocation_managed_funds = models.FloatField(validators=PERCENTAGE_VALIDATOR)
    allocation_other = models.FloatField(validators=PERCENTAGE_VALIDATOR)

    short_term_tax_rate = models.FloatField(validators=PERCENTAGE_VALIDATOR)
    long_term_tax_rate = models.FloatField(validators=PERCENTAGE_VALIDATOR)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ("user",)


class BankAccount(Timestamp):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    bank = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    balance = models.FloatField()
    interest_rate = models.FloatField(validators=PERCENTAGE_VALIDATOR)

    def __str__(self):
        return f"{self.bank} - {self.account_name}"


class Etf(Timestamp):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    ticker = models.CharField(max_length=100)
    fund_name = models.CharField(max_length=100)
    units_held = models.FloatField()
    average_cost = models.FloatField()

    def __str__(self):
        return f"{self.fund_name} - {self.ticker}"


class EtfTransaction(Timestamp):
    etf = models.ForeignKey(Etf, on_delete=models.CASCADE)

    CHOICES = ((0, "Buy"), (1, "Sell"))
    transaction_type = models.PositiveSmallIntegerField(choices=CHOICES)
    order_date = models.DateField()
    units = models.FloatField()
    order_cost = models.FloatField()
    brokerage = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.etf} - {self.units} - {self.order_cost} - {self.transaction_type}"


class Superannuation(Timestamp):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    provider = models.CharField(max_length=100)
    investment_plan = models.CharField(max_length=100)
    balance = models.FloatField()
    market_returns = models.FloatField()
    voluntary_contributions = models.FloatField()

    def __str__(self):
        return f"{self.provider} - {self.investment_plan} - {self.user}"
