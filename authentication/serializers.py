# DRF Serializers
from authentication.utils import Util
from rest_framework import serializers

# DRF Simple JWT.
from rest_framework_simplejwt.tokens import RefreshToken

# Password Reset Token.
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.utils.encoding import DjangoUnicodeDecodeError, force_str, smart_str, smart_bytes

# Encoding and Decoding.
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

# Custom Models.
from .models import User

# Get frontend URL.
from django.contrib.sites.shortcuts import get_current_site

# Reverse URL
from django.urls import reverse

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

class RequestPasswordResetSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['email']

    def validate(self, obj):
        email = obj['data'].get('email', '')

class SetNewUserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    token = serializers.CharField(write_only=True)
    uidb64 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['password', 'token', 'uidb64']

    def validate(self, obj):
        try:
            password = obj.get('password')
            token = obj.get('token')
            uidb64 = obj.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid. Try again.', 401)

            user.set_password(password)

            user.save()

            email_body = f'Hello.\nWe have successfully reset your password.\nUse the newly set password to board the platform.\nWelcome back to Mbuzi Loyalty Program.'
            data = {
                'email_subject': 'Password Reset Successfully.',
                'email_body': email_body,
                'to_email': user.email 
            }

            Util.send_email(data)

            return user

        except Exception as e:
            raise AuthenticationFailed('Something terrible happened. Please try resetting your password again.', 400)

        return super().validate(obj)

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
            raise AuthenticationFailed('Account is not active. Check your email and verify your account to access the platform')
        
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified. Check your email and verify your account to access the platform')
            
        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens
        }






