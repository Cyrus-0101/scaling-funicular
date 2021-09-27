# Unit Test
from order.serializers import OrderSerializer
from django.test import TestCase

# User Model
from django.contrib.auth import get_user_model

# Models.
from order.models import Order, OrderItem, ShippingAddress
from product.models import Category, Product

# Create your tests here.

# Order Tests.
class OrderTests(TestCase):
    """
        Test to create new Order.
    """
    def setUp(self):
        db = get_user_model()           # Get Active User Model
        super_user = db.objects.create_superuser(
            'test@superuser.com',       # Email
            'Username',                 # Username
            'pass123'                   # Password
        )

        Order.objects.create(
            user=super_user,
            paymentMethod="PayPal",
            vatPrice=10.00,
            digitalservicetaxPrice=5.00,
            shippingPrice=0.00,
            totalPrice=1000.00,
            isPaid=True,
            paidAt="2021-09-15 16:49:47.315929+00:00",
            isDelivered=False,

        )

    def test_new_order(self):
        order = Order.objects.get(user=1)

        self.assertEqual(str(order), "Username")

# OrderItem Tests.
class OrderItemTests(TestCase):
    """
        Test to create new OrderItem.
    """
    def setUp(self):
        db = get_user_model()           # Get Active User Model
        super_user = db.objects.create_superuser(
            'test@superuser.com',       # Email
            'Username',                 # Username
            'pass123'                   # Password
        )

        order = Order.objects.create(
            user=super_user,
            paymentMethod="PayPal",
            vatPrice=10.00,
            digitalservicetaxPrice=5.00,
            shippingPrice=0.00,
            totalPrice=1000.00,
            isPaid=True,
            paidAt="2021-09-15 16:49:47.315929+00:00",
            isDelivered=False,

        )

        category = Category.objects.create(name="Category Name")
        product = Product.objects.create(
            user=super_user,
            name="Review Name",
            category=category,
            description="Really cool",
            price=1000.00,
        )

        OrderItem.objects.create(
            product=product,
            order=order,
            name=product.name,
            qty=1,
            price=product.price,
            image=product.image
        )

        OrderSerializer.get_orderItems(self, order)
        OrderSerializer.get_shippingAddress(self, order)
        # OrderSerializer.get_user(self, order)

    def test_new_order_item(self):
        orderItem = OrderItem.objects.get(_id=1)

        self.assertEqual(str(orderItem), orderItem.product.name)

# Shipping Address Tests.
class ShippingAddressTests(TestCase):
    """
        Test to create new Shipping Address.
    """
    def setUp(self):
        db = get_user_model()           # Get Active User Model
        super_user = db.objects.create_superuser(
            'test@superuser.com',       # Email
            'Username',                 # Username
            'pass123'                   # Password
        )

        order = Order.objects.create(
            user=super_user,
            paymentMethod="PayPal",
            vatPrice=10.00,
            digitalservicetaxPrice=5.00,
            shippingPrice=0.00,
            totalPrice=1000.00,
            isPaid=True,
            paidAt="2021-09-15 16:49:47.315929+00:00",
            isDelivered=False,
        )

        ShippingAddress.objects.create(
            order=order,
            address="Address",
            city="City",
            postalCode="00101",
            county="County",
            shippingPrice=order.shippingPrice,
            phoneNumber="+254740673050"
        )

        
    def test_new_shipping_address(self):
        shippingAddress = ShippingAddress.objects.get(_id=1)

        self.assertEqual(str(shippingAddress), shippingAddress.address)

