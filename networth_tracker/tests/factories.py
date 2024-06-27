from django.contrib.auth import get_user_model
from factory import SubFactory
from factory.django import DjangoModelFactory
from faker import Faker

from networth_tracker.models import Account, BankAccount, Etf, EtfTransaction, Superannuation

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
    is_staff = False


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
    date_of_birth = fake.date_of_birth()

    salary = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    eoy_cash_goal = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    emergency_fund = fake.pyfloat(left_digits=2, right_digits=2, positive=True)

    allocation_intensity = fake.random_int(min=0, max=2)
    allocation_etfs = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    allocation_stocks = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    allocation_cryptocurrency = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    allocation_cash = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    allocation_managed_funds = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    allocation_other = fake.pyfloat(left_digits=2, right_digits=2, positive=True)

    short_term_tax_rate = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    long_term_tax_rate = fake.pyfloat(left_digits=2, right_digits=2, positive=True)


class EtfFactory(DjangoModelFactory):
    class Meta:
        model = Etf

    user = SubFactory(CustomUserFactory)
    ticker = fake.word()
    fund_name = fake.word()
    units_held = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    average_cost = fake.pyfloat(left_digits=2, right_digits=2, positive=True)


class EtfTransactionFactory(DjangoModelFactory):
    class Meta:
        model = EtfTransaction

    etf = SubFactory(EtfFactory)
    transaction_type = fake.random_int(min=0, max=1)
    order_date = fake.date()
    units = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    order_cost = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    brokerage = fake.pyfloat(left_digits=2, right_digits=2, positive=True)


class SuperannuationFactory(DjangoModelFactory):
    class Meta:
        model = Superannuation

    user = SubFactory(CustomUserFactory)
    provider = fake.company()
    investment_plan = fake.word()
    balance = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    market_returns = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    voluntary_contributions = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
