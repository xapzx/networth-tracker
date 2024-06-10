from rest_framework import serializers

from networth_tracker.models import CustomUser


class CustomUserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
