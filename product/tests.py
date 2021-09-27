# Unit Test
from django.test import TestCase

# User Model
from django.contrib.auth import get_user_model

# Models.
from .models import Category, Product, Review

# Create your tests here.

# Category Tests.
class CategoryTests(TestCase):
    """
        Test to create new Category.
    """
    def setUp(self):
        Category.objects.create(name="Category Name")

    def test_new_category(self):
        category = Category.objects.get(name="Category Name")

        self.assertEqual(str(category), 'Category Name')

# Product Tests.
class ProductTests(TestCase):
    """
        Test to create new Product.
    """
    def setUp(self):
        db = get_user_model()           # Get Active User Model
        super_user = db.objects.create_superuser(
            'test@superuser.com',       # Email
            'Username',                 # Username
            'pass123'                   # Password
        )
        category = Category.objects.create(name="Category Name")
        Product.objects.create(
            user=super_user,
            name="Product Name",
            category=category,
            description="Really cool",
            price=1000.00,
        )

    def test_new_product(self):
        product = Product.objects.get(name="Product Name")

        self.assertEqual(str(product), 'Product Name')

# Review Tests.
class ReviewTests(TestCase):
    """
        Test to create new Review.
    """
    def setUp(self):
        db = get_user_model()           # Get Active User Model
        super_user = db.objects.create_superuser(
            'test@superuser.com',       # Email
            'Username',                 # Username
            'pass123'                   # Password
        )
        category = Category.objects.create(name="Category Name")
        product = Product.objects.create(
            user=super_user,
            name="Review Name",
            category=category,
            description="Really cool",
            price=1000.00,
        )
        Review.objects.create(
            product=product,
            user=super_user,
            name="Review Name",
            rating=4.5,
            comment="Really cool",
        )

    def test_new_review(self):
        review = Review.objects.get(name="Review Name")

        self.assertEqual(str(review), review.comment)

