"""incomeapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

# Documentation.
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

description = "This is the Official API and Documentation of the Mbuzi Munch Loyalty Program. This program allows users to register, order in-house with payments, accrew and redeem points, among many other functions. More details below."

schema_view = get_schema_view(
   openapi.Info(
      title="Mbuzi Munch API",
      default_version='v1',
      description=description,
      terms_of_service="https://www.mbuzimunch.com/policies/terms/",
      contact=openapi.Contact(email="developers@mbuzimunch.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('product/', include('product.urls')),
    path('order/', include('order.urls')),
    path('loyalty-point/', include('loyalty_point.urls')),

    url('swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
