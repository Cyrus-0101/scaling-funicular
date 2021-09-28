# Paginator
from product.pagination import StandardResultsSetPagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Generic API View, HTTP Status Codes, Views.
from rest_framework import generics, status, views

# permission classes decorators.
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Response.
from rest_framework.response import Response

# HTTP Status Codes
from rest_framework import status

# Models
from .models import Category, Product, Review

# Serializers
from .serializers import CategorySerializer, ProductSerializer, ReviewSerializer

# Local Time Formatter
from pytz import timezone
from datetime import datetime

# Documentation
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.decorators import api_view, permission_classes

# Constants
local_time_zone = timezone("Africa/Nairobi")

# Visitor Level Access Classes.

"""
    Fucntional Based Views.
"""

@api_view(['GET'])
def getProducts(request):
    """
        All Products Paginated into 5 products per page.
    """
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    products = Product.objects.filter(
        name__icontains=query).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(products, 5)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    if page == None:
        page = 1


    # Refactor

    if not products:
        return Response(
            {'detail': 'Currently no products on the platform yet, contact the admin to add products to the platform.'},
            status=status.HTTP_204_NO_CONTENT
        )

    page = int(page)
    serializer = ProductSerializer(products, many=True)
    return Response({'products': serializer.data, 'page': page, 'pages': paginator.num_pages})

@api_view(['GET'])
def getProduct(request, pk):
    """
        Fetch Single Product Details.
    """

    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getCategories(request):
    """
        All Categories Paginated into 5 categories per page.
    """
    query = request.query_params.get('keyword')
    if query == None:
        query = ''

    categories = Category.objects.filter(
        name__icontains=query).order_by('-createdAt')

    page = request.query_params.get('page')
    paginator = Paginator(categories, 5)

    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        categories = paginator.page(1)
    except EmptyPage:
        categories = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = CategorySerializer(categories, many=True)
    return Response(
        {
            'categories': serializer.data,
            'page': page,
            'pages': paginator.num_pages
        }, status=status.HTTP_200_OK
    )

@api_view(['GET'])
def getTopProducts(request):
    products = Product.objects.filter(rating__gte=4).order_by('-rating')[0:5]
    serializer = ProductSerializer(products, many=True)
    if not products:
        return Response(
            {'detail': 'Currently no products reviewed yet, choose a product you want and make a review.'},
            status=status.HTTP_204_NO_CONTENT
        )
    else:
        return Response(
            serializer.data
        )

"""
    Class Based Views
"""
class ProductCreateReviewView(generics.CreateAPIView):

    """
        Authenticated Users can Review Products Once. 
    """

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()

    def post(self, request, pk):
        user = request.data
        product = self.queryset.get(_id=pk)
        data = request.data

        # A user can review a product once.

        alreadyExists = product.review_set.filter(user=user).exists()

        if alreadyExists:
            return Response(
                {'detail': 'Product already reviewed.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        elif data['rating'] == 0:
            return Response(
                {'detail': 'Please select a valid rating'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        else:
            review = Review.objects.create(
                user=user,
                product=product,
                name=user.username,
                rating=data['rating'],
                comment=data['comment']
            )

            reviews = product.review_set.all()
            product.numReviews = len(reviews)

            total = 0
            for i in reviews:
                total += i.rating

            product.rating = total/len(reviews)

            serializer = self.serializer_class(data=product, many=False)
            serializer.is_valid(raise_exception=True)


            product.save()

            return Response(
                {'detail': 'Review Successfully Added.'},
                status=status.HTTP_201_CREATED    
            )

# Admin User Level Access Classes.

# =========================================================== #
# ==================    ADMIN ROUTES    ===================== #
# =========================================================== #

class CategoryCreateAdminView(generics.CreateAPIView):

    """
        Administrator Users can create a Category. 
    """

   
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

    def post(self, request):
        category = request.data

        category = Category.objects.create(
            name=category.name,
        )

        serializer = self.serializer_class(data=category, many=False)
        serializer.is_valid(raise_exception=True)

        return Response(
            {'detail': 'Successfully created category.'},
            status=status.HTTP_201_CREATED
        )

class CategoryUpdateAdminView(generics.UpdateAPIView):

    """
        Administrator Users can update a Category. 
    """

   
    serializer_class = CategorySerializer
    queryset = Category.objects.filter()
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        paidAt = local_time_zone.localize(datetime.now())

        category_data = request.data
        category = self.queryset(_id=pk)
        category.name = category_data['name']
        category.updatedAt = paidAt.astimezone(local_time_zone)

        serializer = self.serializer_class(data=category, many=False)
        serializer.is_valid(raise_exception=True)

        category.save()

class CategoryDeleteAdminView(generics.DestroyAPIView):

    """
        Administrator Users can delete a Category. 
    """

    def delete(self, pk):
        category = Category.objects.get(_id=pk)
        category.delete()

        return Response(
            {'detail': 'Product deleted successfully.'},
            status=status.HTTP_202_ACCEPTED
        )

class ProductCreateAdminView(generics.CreateAPIView):

    """
        Administrator Users can create a Product. 
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    
    def post(self, request):
        user = request.user
        product = request.data
        product_image = request.FILES.get('image')

        product = Product.objects.create(
            user=user,
            name=product.name,
            image=product_image,
            brand=product.brand,
            category=product.category,
            countInStock=product.countInStock,
            description=product.description,
            price=product.price
        )

        serializer = self.serializer_class(data=product, many=False)
        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

class ProductUpdateAdminView(generics.UpdateAPIView):

    """
        Administrator Users can update a Product. 
    """

    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]
    
    def put(self, request, pk):
        paidAt = local_time_zone.localize(datetime.now())

        product_data = request.data
        product_image = request.FILES.get('image')

        product = Product.objects.get(_id=pk)
        product.name = product_data['name']
        product.price = product_data['price']
        product.brand = product_data['brand']
        product.image = product_image
        product.updatedAt = paidAt.astimezone(local_time_zone)
        product.countInStock = product_data['countInStock']
        product.category = product_data['category']
        product.description = product_data['description']

        serializer = self.serializer_class(data=product, many=False)
        serializer.is_valid(raise_exception=True)

        product.save()

        serializer = ProductSerializer(product, many=False)
        serializer.is_valid(raise_exception=True)
        
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

class ProductDeleteAdminView(generics.DestroyAPIView):
    def delete(self, pk):
        product = Product.objects.get(_id=pk)
        product.delete()

        return Response(
            {'detail': 'Product deleted successfully.'},
            status=status.HTTP_202_ACCEPTED
        )






