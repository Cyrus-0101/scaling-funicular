# PUT API Abstraction
from rest_framework.permissions import IsAdminUser
from loyalty_point.serializers import LoyaltyPointTransactionSerializer
from django.core.exceptions import ValidationError
from loyalty_point.models import LoyaltyPoint, LoyaltyPointTransaction
from rest_framework.generics import UpdateAPIView

# REST Framework Decorators.
from rest_framework.response import Response

# User Model.
from authentication.models import User

# Status Code Error Handling
from rest_framework import status

# Local Time Formatter
from pytz import timezone
from datetime import datetime
from decimal import Decimal

# Constants.
local_time_zone = timezone("Africa/Nairobi")
base_loyalty_conversion_rate = 150.00

# Formatting stored time to be Kenyan UTC +3 Local Time
currentTime = local_time_zone.localize(datetime.now())

# Create your views here.
class UpdateLoyaltyPointValueFromPos(UpdateAPIView):
    '''
       Redeem or Accrew Loyalty Points from POS Route.
    '''
    serializer_class = LoyaltyPointTransactionSerializer
    permission_classes = [IsAdminUser]

    def put(self, request, idx):
        data = request.data

        transactionPrice = data['amount']
        transactionType = data['transactionType']

        # Get User Object using User ID passed from URL.
        user = User.objects.get(id=idx)

        if transactionType == None:
            raise ValidationError(
                {'detail': 'Unacceptable request, please try again.'},
                status = status.HTTP_406_NOT_ACCEPTABLE
            )

        if transactionPrice == 0:
            raise ValidationError(
                {'detail': 'No Order Items Found. Buy Something to get loyalty points.'},
                status = status.HTTP_400_BAD_REQUEST
            )

        # 1. Calculate Loyalty Point to Money Value:
        # One User can have multiple points, how can I keep track of all users points 

        accrewPoints = transactionPrice / base_loyalty_conversion_rate # This is in LoyaltyPoint
        redeemPoints = (transactionPrice / base_loyalty_conversion_rate) / 1 # This is in Kshs.
        
        # Create Loyalty Point Object.
        loyalty_point = LoyaltyPoint.objects.get(user = user)
        
        # Check type of transaction and assign points accordingly in an if ... elif statement.
        # Saving the Loyalty Point Object Accordingly.
        if transactionType == 'accrew':

            # Create loyalty point transaction Object.
            loyalty_point_transaction = LoyaltyPointTransaction.objects.create(
                loyaltyPoint = loyalty_point,
                transactionPoints = accrewPoints,
                transactionType = transactionType,
                transactionPrice = transactionPrice,
                createdAt = currentTime,
            )

            loyalty_point_transaction.save()
            loyalty_point.totalPoints += Decimal(accrewPoints)
            
            
            serializer = self.serializer_class(data=loyalty_point_transaction, many=False)
            serializer.is_valid(raise_exception=True)

            loyalty_point.save()

            return Response(
                {'detail': f"Successfully accredited {accrewPoints} to {loyalty_point.user.first_name}'s account. Thank you for choosing Mbuzi Munch."},
                status = status.HTTP_202_ACCEPTED
            )
            
        elif transactionType == 'redeem':

            if loyalty_point.totalPoints < 200 or transactionPrice > loyalty_point.totalPoints:
                return Response(
                    {'detail': 'Unable to redeem points. Keep shopping to get more points :).'},
                    status = status.HTTP_406_NOT_ACCEPTABLE
                )

            else:
                # Create loyalty point transaction Object.
                loyalty_point_transaction = LoyaltyPointTransaction.objects.create(
                    loyaltyPoint = loyalty_point,
                    transactionPoints = redeemPoints,
                    transactionType = transactionType,
                    transactionPrice = transactionPrice,
                    redeemedAt = currentTime,
                )

                loyalty_point.totalPoints -= Decimal(redeemPoints)

                serializer = self.serializer_class(data=loyalty_point_transaction, many=False)
                serializer.is_valid(raise_exception=True)

                loyalty_point.save()

                return Response(
                    {'detail': f"Successfully deducted {redeemPoints} from {loyalty_point.user.first_name}'s account, worth {round(redeemPoints, 2)} Kshs. Keep shopping with us."},
                    status = status.HTTP_202_ACCEPTED
                )

        else:
            return Response(
                {'detail': 'Something wrong happened. Try checking your enums.'},
                status = status.HTTP_400_BAD_REQUEST
            )



