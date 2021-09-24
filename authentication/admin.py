# # Django Modules.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# User Model
from authentication.models import User

# Admin Page Configuration.
class UserAdminConfig(UserAdmin):
    model = User
    search_fields = [
        'email',
        'username',
        'is_active',
        'is_staff',
        'is_verified'
    ]
    list_filter = [
        'is_active',
        'is_staff',
        'is_verified'
    ]
    ordering = ['date_joined']
    list_display = [
        'email',
        'username',
        'is_active',
        'is_staff',
        'date_joined'
    ]

    fieldsets = [
        ('User Details', {'fields': ('email', 'username', 'is_verified')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser',)}),
        ('Personal', {'fields': ('birthday', 'last_login',)})
    ]

    add_fieldsets = [
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'username',
                'password1',
                'password2',
                'birthday',
                'is_active',
                'is_staff',

            )
        })
    ]


# Register your models here.
admin.site.register(User, UserAdminConfig)