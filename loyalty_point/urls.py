from django.urls import path
from .views import UpdateLoyaltyPointValueFromPos

urlpatterns = [
    path('<int:idx>/add-from-pos/', UpdateLoyaltyPointValueFromPos.as_view(), name='put-loyalty-points-from-POS'),

]