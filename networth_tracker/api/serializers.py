from rest_framework import serializers

from networth_tracker.models import Account, BankAccount, CustomUser


class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account
        fields = "__all__"


class BankAccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = BankAccount
        fields = "__all__"
        read_only_fields = ("id", "user")
