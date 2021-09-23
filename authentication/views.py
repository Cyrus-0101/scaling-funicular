import os

# Generic API View, HTTP Status Codes, Views.
from rest_framework import generics, status, views

# JWT
import jwt

from django.conf import settings

# il8n
from django.utils.translation import gettext as _

# DRF JSON Response Serializer
from rest_framework.response import Response

# Serializers.
from .serializers import EmailVerificationSerializer, RegisterSerializer, LoginSerializer

# Tokens.
from rest_framework_simplejwt.tokens import RefreshToken

# Reverse URL
from django.urls import reverse

# Models.
from .models import User

# Helper Classes.
from .utils import Util

# Get frontend URL.
from django.contrib.sites.shortcuts import get_current_site

# Documentation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain

        relativeLink = reverse('email-verify')

        absUrl = 'http://'+current_site+relativeLink+'?token='+str(token)

        email_body = f'Hi {user.username}.\nWelcome To Mbuzi Munch Loyalty Program.\nUse the link below to verify your email: \n{absUrl}'
        data = {
            'email_subject': 'Verify your Email Address.',
            'email_body': email_body,
            'to_email': user.email 
        }

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):
    
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'Token',
        in_=openapi.IN_QUERY,
        description="Enter token to validate email.",
        type=openapi.TYPE_STRING
    )

    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        
        try:
            payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms="HS256")
            
            user = User.objects.get(id=payload['user_id'])

            if user.is_active:
                return Response(
                    {'detail': 'Email Address already activated. Try logging in to the app again.'},
                    status=status.HTTP_208_ALREADY_REPORTED
                )
            
            if not user.is_active:
                user.is_active = True
                user.is_verified = True

                user.save()

            email_body = f'Hi {user.username}.\nWelcome To Mbuzi Munch Loyalty Program. You have successfully activated your account.\nCheckout our App and be able to order in-house. Thank you for choosing Mbuzi :): \n'
            
            data = {
                'email_subject': 'Welcome! Successfully Activated Account.',
                'email_body': email_body,
                'to_email': user.email
            }

            Util.send_email(data)

            return Response(
                {'detail': 'Successfully Activated Email Address.'},
                status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {'error': 'Token  Expired.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {'error': 'Invalid Token.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)






















# class RegisterView(generics.GenericAPIView):

#     serializer_class = RegisterSerializer

#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         user_data = serializer.data
#         user = User.objects.get(email=user_data['email'])

#         token = RefreshToken.for_user(user).access_token

#         current_site = get_current_site(request).domain

#         relativeLink = reverse('email-verify')

#         absurl = 'http://'+current_site+relativeLink+'?token='+str(token)

#         email_body = f'Hi {user.username}.\nWelcome To Mbuzi Munch Loyalty Program.\nUse the link below to verify your email: \n{absurl}'
#         data = {
#             'email-subject': 'Verify your Email Address.',
#             'email-body': email_body,
#             'to-email': user.email 
#         }

#         Util.send_email(data)

#         return Response(user_data, status=status.HTTP_201_CREATED)

# class VerifyEmail(views.APIView):
    
#     serializer_class = EmailVerificationSerializer

#     token_param_config = openapi.Parameter(
#         'Token',
#         in_=openapi.IN_QUERY,
#         description="Enter token to validate email.",
#         type=openapi.TYPE_STRING
#     )

    
#     @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.GET.get('token')
        
#         try:
#             payload = jwt.decode(token, os.environ.get('SECRET_KEY'), algorithms="HS256")
            
#             user = User.objects.get(id=payload['user_id'])
            
#             if not user.is_verified:
#                 user.is_verified = True

#                 user.save()

#             email_body = f'Hi {user.username}.\nWelcome To Mbuzi Munch Loyalty Program. You have successfully activated your account.\nCheckout our App and be able to order in-house. Thank you for choosing Mbuzi :): \n'
#             data = {
#                 'email-subject': 'Welcome! Successfully Activated Account.',
#                 'email-body': email_body,
#                 'to-email': user.email 
#             }

#             Util.send_email(data)


#             return Response(
#                 {'detail': 'Successfully Activated Email Address.'},
#                 status=status.HTTP_200_OK
#             )
#         except jwt.ExpiredSignatureError as identifier:
#             return Response(
#                 {'error': 'Token  Expired.'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         except jwt.exceptions.DecodeError as identifier:
#             return Response(
#                 {'error': 'Invalid Token.'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

# class LoginView(generics.GenericAPIView):
    
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


