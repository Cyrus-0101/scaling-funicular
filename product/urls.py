from django.urls import path

from .views import CategoryCreateAdminView, CategoryDeleteAdminView, CategoryUpdateAdminView, ProductCreateAdminView, ProductCreateReviewView, ProductDeleteAdminView, ProductUpdateAdminView, getCategories, getProduct, getProducts, getTopProducts

urlpatterns = [
    
    path('', getProducts, name="get-products"),
    path('categories/', getCategories, name="get-categories"),    
    
    path('<str:pk>/reviews/', ProductCreateReviewView.as_view(), name="post-product-review"),
    path('top-products/', getTopProducts, name="get-top-products"),
    path('<str:idx>/', getProduct, name="product"),

    path('create-category/', CategoryCreateAdminView.as_view(), name="admin-create-product"),
    path('update-category/<str:pk>/', CategoryUpdateAdminView.as_view(), name="admin-update-categpry"),
    path('delete/<str:idx>/', CategoryDeleteAdminView.as_view(), name="admin-delete-product"),


    path('create/', ProductCreateAdminView.as_view(), name="admin-create-product"),
    path('update/<str:idx>/', ProductUpdateAdminView.as_view(), name="admin-update-product"),
    path('delete/<str:idx>/', ProductDeleteAdminView.as_view(), name="admin-delete-product"),

]




