# Validators.
from django.core.validators import MaxValueValidator

# Models.
from django.db import models

# User Model.
from authentication.models import User

# # Create your models here.
# class Brand(models.Model):
#     name = models.CharField(max_length=50, null=True)
#     createdAt = models.DateTimeField(auto_now_add=True)
#     _id = models.AutoField(primary_key=True, editable=False)

#     class Meta:
#         ordering = ['name']
        
#     def __str__(self):
#         return str(self.name)

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=50, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return str(self.name)

# Product Model
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='menu_images/', default='/sample.jpg')
    # brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(null=True, blank=True, auto_now_add=False)
    description = models.TextField(max_length=250, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)
    rating = models.DecimalField(null=True, blank=True, max_digits=7, decimal_places=1)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return str(self.name)


# Review Model.
# Parent Child Relationship.
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    rating = models.DecimalField(null=True, blank=True, default=0, max_digits=2, decimal_places=1, validators=[
        MaxValueValidator(5.0)
    ])
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    class Meta:
        ordering = ['rating']

    def __str__(self):
        return str(self.comment)
