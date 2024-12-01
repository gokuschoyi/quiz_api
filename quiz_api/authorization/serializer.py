from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "password", "date_joined"]
        read_only_fields = ["id", "date_joined"]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    class Meta:
        model: CustomUser
        fields = ["email", "password"]
        read_only_fields = ["email", "password"]