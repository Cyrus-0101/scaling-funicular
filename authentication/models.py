from django.db import models

# Base User Abstractions.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# il8n
from django.utils.translation import gettext as _

# Manager.
class UserManager(BaseUserManager):

    def create_user(self, username, email, password):
        if username is None:
            raise TypeError(_('Username is required for a user to sign up.'))

        if email is None:
            raise TypeError(_('Email is required for a user to sign up.'))

        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, username, email, password, **otherfields):
        if username is None:
            raise TypeError(_('Username is required for a user to sign up.'))

        if password is None:
            raise TypeError(_('Password is required for a user to sign up.'))

        if email is None:
            raise TypeError(_('Email is required for a user to sign up.'))
        
        otherfields.setdefault('is_staff', True)
        otherfields.setdefault('is_superuser', True)
        otherfields.setdefault('is_active', True)

        if otherfields.get('is_staff') is not True:
            raise TypeError(_("Super users must be staff."))

        if otherfields.get('is_superuser') is not True:
            raise TypeError(_("Super users must be super users."))
        
        if otherfields.get('is_active') is not True:
            raise TypeError(_("Super users must have be active."))

        user = self.create_user(email, username, password, **otherfields)

        return user


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    AUTH_TYPE_OPTIONS = [
        ('google', 'Google'),
        ('twitter', 'Twitter'),
        ('facebook', 'Facebook'),
        ('email', 'Email'),
    ]
    
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="Date joined", auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    birthday = models.DateTimeField(verbose_name="Birthday", auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return str(self.email)

    # def tokens(self):
    #    return pass

