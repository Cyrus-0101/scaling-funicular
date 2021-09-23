# Models
from .models import Order, OrderItem, ShippingAddress

# Product Model
from product.models import Product

# Loyalty Point Model.
from loyalty_point.models import LoyaltyPoint, LoyaltyPointTransaction

# Loyalty Point Model.
from loyalty_point.serializers import LoyaltyPointSerializer, LoyaltyPointTransactionSerializer

# Error Handling.
from django.core.exceptions import ValidationError

# Custom Serializers
from .serializers import OrderItemSerializer, OrderSerializer

# REST Framework Decorators.
from rest_framework.response import Response

# Restricted API Routes decoraters & classes.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Status Code Error Handling
from rest_framework import status

# Decimal Data Formatting
from decimal import Decimal

# Local Time Formatter
from pytz import timezone
from datetime import datetime

# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Documentation.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.generics import CreateAPIView, UpdateAPIView

# Create your views here...

# =========================================================== #
# ==================    ORDER ROUTES    ===================== #
# =========================================================== #

# Constants. 
local_time_zone = timezone("Africa/Nairobi")
test_param = openapi.Parameter('Token', openapi.IN_QUERY, description="Enter User Access Token to get Authorization.", type=openapi.TYPE_BOOLEAN)
user_response = openapi.Response('Response description:', OrderSerializer)


class UserAddOrderItems(CreateAPIView):

    """
        Logged in users can create an order and add order items.
    """

    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        data = request.data
        orderItems = data['orderItems']

        if orderItems and len(orderItems) == 0:
            raise ValidationError('No Order Items Found. Add items to your shopping cart before proceeding.')


        else:
            # 1. Create Order.
            order = Order.objects.create(
                user = user,
                paymentMethod = data['paymentMethod'],
                vatPrice = data['vatPrice'],
                digitalservicetaxPrice = data['digitalservicetaxPrice'],
                shippingPrice = data['shippingPrice'],
                totalPrice = data['totalPrice']
            )

            # 2. Create Shipping Address.
            shipping = ShippingAddress.objects.create(
                order = order,
                address = data['shippingAddress']['address'],
                city = data['shippingAddress']['city'],
                postalCode = data['shippingAddress']['postalCode'],
                county = data['shippingAddress']['county'],
                phoneNumber = data['shippingAddress']['phoneNumber'],
                shippingPrice=data['shippingPrice']
            )

            # 3. Create OrderItems and set order to orderItem relationship.
            for i in orderItems:

                product = Product.objects.get(_id = i['product'])

                item = OrderItem.objects.create(
                    product = product,
                    order = order,
                    name = product.name,
                    qty = i['qty'],
                    price = product.price,
                    image = product.image.url
                )

                # 4. Update Product CountIn Stock.
                product.countInStock -= item.qty
                product.save()


            serializer = self.serializer_class(order, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

# GET Order By ID.
@swagger_auto_schema(method='get', responses={200: user_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_by_id(request, pk):
    '''
       Gets Order Information by ID.
    '''
    user = request.user
    order = Order.objects.get(_id = pk)
    
    try:

        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            serializer.is_valid(raise_exception=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            Response(
                {'detail': "You are not Authorized to View this Page." },
                status = status.HTTP_401_UNAUTHORIZED
            )
           
    except:
        return Response(
            { 'detail': 'Order Does Not Exist. Try Again.' },
            status = status.HTTP_404_NOT_FOUND
        )


class UserUpdateOrderToPaid(UpdateAPIView):

    """
        Users pay for their orders and change their order status to Paid. 
    """

    serializer_class = [OrderSerializer]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):

        order = Order.objects.get(_id = pk)

        base_loyalty_conversion_rate = 200.00
        # The above means that 200 ksh translates to 1 loyalty point.

        # Formatting stored time to be Kenyan UTC +3 Local Time
        paidAt = local_time_zone.localize(datetime.now())

        transactionType = order.paymentMethod

        user = order.user

        totalPoints = order.totalPrice / base_loyalty_conversion_rate

        # Create Loyalty Point Object.
        loyalty_point = LoyaltyPoint.objects.get(user = user)

        if transactionType == 'RedeemPoints':

            # Create loyalty point transaction Object.
            loyalty_point_transaction = LoyaltyPointTransaction.objects.create(
                loyaltyPoint = loyalty_point,
                transactionPoints = totalPoints,
                transactionType = transactionType,
                transactionPrice = order.totalPrice,
                createdAt = paidAt,
            )

            loyalty_point_transaction.save()

            # In order for us to have an accurate creditation we need to have 
            # to convert the price again to points then from points to money.

            redeemPoints = totalPoints / 1

            # In the above transaction we deal with the total price after it has been converted to points and 
            # the convert it to money at the rate of 1 loyalty point == 1 ksh

            loyalty_point.redeemedAt = paidAt
            loyalty_point.totalPoints -= Decimal(redeemPoints)

            order.isPaid = True

            order.paidAt = paidAt.astimezone(local_time_zone)

            serializer = self.serializer_class(order, many=False)
            serializer.is_valid(raise_exception=True)
            
            order.isPaid = True
            order.save()

            loyalty_point.save()

            return Response(f'Order was paid successfully. Deducted {totalPoints}, from your account. Keep shopping to boost your points.', status=status.HTTP_202_ACCEPTED)

        elif transactionType == 'Mpesa' or 'PayPal' or 'Equity':
            order.paidAt = paidAt.astimezone(local_time_zone)

            serializer = self.serializer_class(order, many=False)
            serializer.is_valid(raise_exception=True)

            order.save()

            return Response(f'Order was paid successfully. Accredited {totalPoints}, to your points. Keep shopping to get more points.', status=status.HTTP_202_ACCEPTED)

        else:
            return Response(
                {'detail': 'Something wrong happened. Try checking your enums.'},
                status = status.HTTP_400_BAD_REQUEST
            )


# GET My Orders.
@swagger_auto_schema(method='get', responses={200: user_response})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_orders(request):
    '''
       Users can get all their orders on the profile page.
    '''
    user = request.user

    orders = user.order_set.all()

    serializer = OrderSerializer(orders, many=True)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK  
    )



# =========================================================== #
# ==================    ADMIN ROUTES    ===================== #
# =========================================================== #

# GET Admin Orders.
@swagger_auto_schema(method='get', responses={200: user_response})
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_orders(request):
    '''
        Admin User can get All Orders on the System.
    '''
    orders = Order.objects.all()

    page = request.query_params.get('page')
    paginator = Paginator(orders, 5)

    try:
        orders = paginator.page(page)
    
    except PageNotAnInteger:
        orders = paginator.page(1)

    except EmptyPage:
        orders = paginator.page(paginator.num_pages)

    if page == None:
        page = 1
    
    page = int(page)
  
    serializer = OrderSerializer(orders, many=True)
    return Response({
        'orders': serializer.data,
        'page': page,
        'pages': paginator.num_pages,
    }, status=status.HTTP_200_OK)


class OrderAdminDeliverProduct(UpdateAPIView):
    '''
        Admins (Staff) can change the status of the order to deliverred.
    '''
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, idx):

        order = Order.objects.get(_id=idx)

        order.isDelivered = True

        deliveredAt = local_time_zone.localize(datetime.now())

        order.deliveredAt = deliveredAt.astimezone(local_time_zone)

        serializer = OrderSerializer(order, many=False)
        serializer.is_valid(raise_exception=True)
        
        order.save()

        return Response(serializer.data)


