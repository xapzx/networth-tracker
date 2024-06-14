from django.contrib.auth import get_user_model
from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from networth_tracker.models import Account, BankAccount

# initialise the faker with en_AU locale
fake = Faker("en_AU")


class CustomUserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ("email",)

    email = fake.email()
    password = fake.password(
        length=12, special_chars=True, digits=True, upper_case=True, lower_case=True
    )
    is_verified = True
    is_active = True


class BankAccountFactory(DjangoModelFactory):
    class Meta:
        model = BankAccount

    user = SubFactory(CustomUserFactory)
    bank = fake.company()
    account_name = fake.word()
    balance = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    interest_rate = fake.pyfloat(left_digits=2, right_digits=2, positive=True)


class AccountFactory(DjangoModelFactory):
    class Meta:
        model = Account

    user = SubFactory(CustomUserFactory)
    first_name = fake.first_name()
    last_name = fake.last_name()
