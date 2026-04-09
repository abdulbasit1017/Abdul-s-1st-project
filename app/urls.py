from django.urls import path
from .views import ProductAPI

urlpatterns = [
    path('products/', ProductAPI.as_view(),name='products'),
    path('products/<int:id>/', ProductAPI.as_view(),name='product-detail'),
]