from django.urls import path
from .views import RegisterView, VerifyEmail

urlpatterns = [
    # path('login/', views.MyTokenObtainPairView.as_view(), name='login-user'),
    path('register/', RegisterView.as_view(), name="register-user"),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

    # path('profile/', views.get_user_profile, name="user-profile"),
    # path('profile/update/', views.update_user_profile, name="update-user-profile"),

    # path('', views.admin_get_users, name="all-users"),
    # path('<str:pk>/', views.admin_get_user_by_id, name="delete-user"),
    # path('delete/<str:pk>/', views.admin_delete_user, name="delete-user"),
    # path('update/<str:pk>/', views.admin_update_user_profile, name="delete-user"),
    

]