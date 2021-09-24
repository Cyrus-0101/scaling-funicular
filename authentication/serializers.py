# DRF Serializers
from rest_framework import serializers

# DRF Simple JWT.
from rest_framework_simplejwt.tokens import RefreshToken

# Custom Models.
from .models import User

# Utils.
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

# Input Validator
from rest_framework.validators import UniqueTogetherValidator

# Serializers.

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    isSuperUser = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    default_error_messages = {
        'username': 'The username should only contain alphanumeric characters'
    }

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'isAdmin', 'isSuperUser', 'password']

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
        

class UserSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)
    isSuperUser = serializers.SerializerMethodField(read_only=True)
        
    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'isAdmin', 'isSuperUser']

    def get__id(self, obj):
        return obj.id

    def get_username(self, obj):
        return obj.username

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_isSuperUser(self, obj):
        return obj.is_superuser

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(
        max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj['email'])

        return {
            'refresh': user.tokens()['refresh'],
            'access': user.tokens()['access']
        }

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, obj):
        email = obj.get('email', '')
        password = obj.get('password', '')
        # filtered_user_by_email = User.objects.filter(email=email)
        user = authenticate(email=email, password=password)

        # if filtered_user_by_email.exists() and filtered_user_by_email[0].auth_provider != 'email':
        #     raise AuthenticationFailed(
        #         detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
            
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }


