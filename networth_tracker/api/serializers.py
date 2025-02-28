from rest_framework import serializers

from networth_tracker.models import (
    Account,
    BankAccount,
    CustomUser,
    Etf,
    EtfTransaction,
    Superannuation,
)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "password")
        read_only_fields = ("id",)
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class AccountSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ("id",)

    def create(self, validated_data, **kwargs):
        user = self.context["request"].user

        # Check if an account already exists for the user
        if Account.objects.filter(user=user).exists():
            raise serializers.ValidationError("An account already exists for this user.")

        return super(AccountSerializer, self).create(validated_data)


class BankAccountSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = "__all__"
        read_only_fields = ("id",)


class EtfSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Etf
        fields = "__all__"
        read_only_fields = ("id", "units_held", "average_cost")

    def validate_ticker(self, value):
        user = self.context["request"].user
        if Etf.objects.filter(ticker=value, user=user).exists():
            raise serializers.ValidationError("Ticker already exists for this user.")
        return value


class EtfTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtfTransaction
        fields = "__all__"
        read_only_fields = ("id",)

    def validate_etf(self, value):
        user = self.context["request"].user

        if not Etf.objects.filter(pk=value.id, user=user).exists():
            raise serializers.ValidationError(
                "Invalid ETF selection. You can only create transactions for ETFs you own."
            )

        return value


class SuperannuationSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Superannuation
        fields = "__all__"
        read_only_fields = ("id",)
