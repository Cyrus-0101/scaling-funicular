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
from .serializers import EmailVerificationSerializer, UserSerializer

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

    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = str(RefreshToken.for_user(user).access_token)

        current_site = get_current_site(request).domain

        relativeLink = reverse('email-verify')

        absurl = f'http://{current_site}{relativeLink}?token={token}'
        print(absurl)
        email_body = f'Hi {user.username}.\nWelcome To Mbuzi Munch Loyalty Program.\nUse the link below to verify your email: \n{absurl}'
        data = {
            'email-subject': 'Verify your Email Address.',
            'email-body': email_body,
            'to-email': user.email 
        }

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token',
        in_=openapi.IN_QUERY,
        description="Enter token to validate email.",
        type=openapi.TYPE_STRING
    )

    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY)
            user = User.objects.get(id=payload['user_id'])
            
            if not user.is_verified:
                user.is_verified = True

                user.save()

            return Response(
                {'email': 'Successfully Activated Email Address.'},
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