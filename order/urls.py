from django.urls import path

# Views.
from .views import OrderAdminDeliverProduct, UserAddOrderItems, UserUpdateOrderToPaid, get_my_orders, get_order_by_id, get_orders

urlpatterns = [
    path('', get_orders, name='admin-get-orders'),
    path('add/', UserAddOrderItems.as_view(), name='add-orders'),
    path('my-orders/', get_my_orders, name='get-my-orders'),

    path('<str:idx>/deliver/', OrderAdminDeliverProduct.as_view(), name='update-order-to-delivered'),

    path('<str:pk>/', get_order_by_id, name='get-order-by-id'),
    path('<str:pk>/pay/', UserUpdateOrderToPaid, name='update-order to paid'),

]