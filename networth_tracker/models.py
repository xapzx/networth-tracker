# networth_tracker/models.py

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Specifies whether the user can log into the Django admin site"),
    )
    is_active = models.BooleanField(_("active status"), default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now())

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email


class Account(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class BankAccount(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    bank = models.CharField(max_length=100)
    account_name = models.CharField(max_length=100)
    balance = models.FloatField()
    interest_rate = models.FloatField()

    def __str__(self):
        return f"{self.bank} - {self.account_name}"
