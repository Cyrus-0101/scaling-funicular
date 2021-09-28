import os
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import DjangoUnicodeDecodeError, smart_bytes, smart_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

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
from .serializers import EmailVerificationSerializer, RegisterSerializer, LoginSerializer, SetNewUserPasswordSerializer, UserSerializer

# Tokens.
from rest_framework_simplejwt.tokens import RefreshToken

# Permission Classes Abstraction & Decorators.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Reverse URL
from django.urls import reverse

# Models.
from .models import User

# Helper Classes.
from .utils import Util

# Get frontend URL.
from django.contrib.sites.shortcuts import get_current_site

# Password Hasher.
from django.contrib.auth.hashers import make_password

# Documentation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Serializers.
from authentication.serializers import LoginSerializer, RequestPasswordResetSerializer

# Create your views here.


#  Func. Based Views.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    """
        Authenticated users can fetch their user information on the platform.
    """
    user = request.user
    serializer = UserSerializer(user, many=False)

    return Response(serializer.data, status=status.HTTP_200_OK)


# =========================================================== #
# ==================    ADMIN ROUTES    ===================== #
# =========================================================== #


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    """
        Admin fetch all Users on the platform.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def adminGetUserById(request, pk):
    """
        Admin fetch User by ID.
    """
    user = User.objects.get(id=pk)

    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

# Class Based Views.
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

class UpdateUserInformation(generics.UpdateAPIView):
    """
        Authenticated users can update their user information on the platform.
    """

    serializer_class = LoginSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects

    def put(self, request, pk):
        user = self.queryset.get(id=pk)
        serializer = LoginSerializer(user, many=False)

        data = request.data
        user.username = data['username']
        user.email = data['email']

        if data['password'] != '':
            user.password = make_password(data['password'])

        user.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class RequestPasswordReset(generics.GenericAPIView):
    """
        Request Password Reset Through Email Token.
    """

    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=data)

        email = request.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request=request).domain

            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            absUrl = 'http://'+current_site+relativeLink+'?token='+str(token)

            email_body = f'Hello.\nWe got a request to reset your password.\nUse the link below to reset your password: \n{absUrl}\n If you did not make this request ignore this email. '
            data = {
                'email_subject': 'Reset Your Password.',
                'email_body': email_body,
                'to_email': user.email 
            }

            Util.send_email(data)

        return Response(
            {'detail': 'We have sent a Reset Password Link, that will expire in 3hrs. Kindly check your email and renew your password.'},
            status=status.HTTP_200_OK
        )

class PasswordTokenCheckAPI(generics.GenericAPIView):

    """
        API Route to validate Password Reset Token.
    """

    serializer_class = RequestPasswordResetSerializer

    def get(self, request, uidb64, token):
        
        try:
            id=smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)


            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {'error': 'Token is not valid, please request a new one.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            return Response(
                {
                    'success': True,
                    'detail': 'Credentials Valid and Accepted.',
                    'uidb64': uidb64,
                    'token' : token 
                },
                status=status.HTTP_202_ACCEPTED
            )

        except DjangoUnicodeDecodeError as identifier:
            return Response(
                    {'error': 'Token is not valid, please request a new one.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )


class SetNewUserPassword(generics.GenericAPIView):
    """
        Sets new user password after successfully decoding token and getting User ID from UIDB64.
    """
    serializer_class = SetNewUserPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            {
                'success': True,
                'message': 'Password Reset Successfully'
            },
            status=status.HTTP_202_ACCEPTED
        )




# =========================================================== #
# ==================    ADMIN ROUTES    ===================== #
# =========================================================== #



# Class Based Views.
class DeleteUser(generics.DestroyAPIView):

    queryset = User.objects
    
    def delete(self, request, pk):
        userForDeletion = self.queryset.get(id=pk)
        userForDeletion.delete()

        return Response('User was successfully deleted.', status=status.HTTP_204_NO_CONTENT)







