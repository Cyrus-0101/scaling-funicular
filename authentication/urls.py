from django.urls import path

# Views.
from .views import DeleteUser, LoginAPIView, PasswordTokenCheckAPI, RegisterView, RequestPasswordReset, SetNewUserPassword, UpdateUserInformation, VerifyEmail, adminGetUserById, getUserProfile, getUsers

# Rest Framework TokenRefresh.
from rest_framework_simplejwt.views import TokenRefreshView

# /auth/

urlpatterns = [

    path('register/', RegisterView.as_view(), name="register-user"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('login/', LoginAPIView.as_view(), name='login-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-email/', RequestPasswordReset.as_view(), name='password-reset-email'),
    path('password-reset-complete/', SetNewUserPassword.as_view(), name='password-reset-complete'),

    path('profile/', getUserProfile, name="user-profile"),
    path('profile/update/', UpdateUserInformation.as_view(), name="update-user-profile"),

    path('admin-users/', getUsers, name="admin-all-users"),
    path('admin-users/<str:pk>/', adminGetUserById, name="admin-get-user-by-id"),
    path('admin/delete/<str:pk>/', DeleteUser.as_view(), name="admin-delete-user"),
    path('admin/update/<str:pk>/', UpdateUserInformation.as_view(), name="admin-update-user"),
    

]