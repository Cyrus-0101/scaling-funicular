# DRF Serializers
from rest_framework import serializers

# DRF Simple JWT.
# from rest_framework_simplejwt.tokens import RefreshToken

# Custom Models.
from .models import User

# Input Validator
from rest_framework.validators import UniqueTogetherValidator

# Serializers.

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    isSuperUser = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'
    }

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'isAdmin', 'isSuperUser','password']

    def validate(self, obj):
        email = obj.get('email', '')
        username = obj.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError(
                self.default_error_messages)
        return obj

    def create(self, obj):
        return User.objects.create_user(**obj)

    def get_isSuperUser(self, obj):
        return obj.is_superuser

    def get_isAdmin(self, obj):
        return obj.is_staff


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)


    class Meta:
        model = User
        fields = ['token']
        