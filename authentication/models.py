from django.db import models

# DRF Simple JWT.
from rest_framework_simplejwt.tokens import RefreshToken

# Base User Abstractions.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# il8n
from django.utils.translation import gettext as _

# Manager.
class UserManager(BaseUserManager):

    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError(_("Users must have an email address."))

        if not username:
            raise ValueError(_("Users must have a username."))

        email=self.normalize_email(email)

        user = self.model(
            email=email,
            username=username,
            **other_fields,
        )   

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, username, password, **otherfields):
        otherfields.setdefault('is_staff', True)
        otherfields.setdefault('is_superuser', True)
        otherfields.setdefault('is_active', True)
        otherfields.setdefault('is_verified', True)

        if otherfields.get('is_staff') is not True:
            raise ValueError(_("Super users must be staff to access the platform."))

        if otherfields.get('is_superuser') is not True:
            raise ValueError(_("Super users must be super users to access the platform."))
        
        if otherfields.get('is_active') is not True:
            raise ValueError(_("Super users must have be active to access the platform."))

        if otherfields.get('is_verified') is not True:
            raise ValueError(_("Super users must have be verified to access the platform."))



        return self.create_user(email, username, password, **otherfields)


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(max_length=30, db_index=True, unique=True)
    email = models.EmailField(db_index=True, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(verbose_name="Date joined", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, editable=True)
    birthday = models.DateTimeField(verbose_name="Birthday", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return str(self.email)

    def tokens(self):
       refresh = RefreshToken.for_user(self)

       return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),

       }


