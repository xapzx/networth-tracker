from rest_framework import serializers

from networth_tracker.models import Account, BankAccount, CustomUser


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


class BankAccountSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = BankAccount
        fields = "__all__"
        read_only_fields = ("id",)
