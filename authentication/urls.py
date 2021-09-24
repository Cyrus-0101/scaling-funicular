from django.urls import path
from .views import DeleteUser, LoginAPIView, RegisterView, UpdateUserInformation, VerifyEmail, adminGetUserById, getUserProfile, getUsers

# /auth/

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register-user"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),
    path('login/', LoginAPIView.as_view(), name='login-user'),

    path('profile/', getUserProfile, name="user-profile"),
    path('profile/update/', UpdateUserInformation.as_view(), name="update-user-profile"),

    path('admin-users/', getUsers, name="admin-all-users"),
    path('admin-users/<str:pk>/', adminGetUserById, name="admin-get-user-by-id"),
    path('admin/delete/<str:pk>/', DeleteUser.as_view(), name="admin-delete-user"),
    path('admin/update/<str:pk>/', UpdateUserInformation.as_view(), name="admin-update-user"),
    

]