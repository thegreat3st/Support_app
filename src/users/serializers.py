from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from src.users.user_constants import Role

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        attrs["password"] = make_password(attrs["password"])
        attrs["role"] = Role.USER

        return attrs


class UserPublicSerializer(serializers.ModelSerializer):
    days_since_joined = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name"]
        
        def get_days_since_joined(self, obj):
            return (now() - obj.date_joined).days