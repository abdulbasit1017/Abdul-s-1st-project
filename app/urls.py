from django.urls import path
from .views import (
    ProductAPI,
    CategoryAPI,
    home_page,
    category_page,
    product_detail,
    cart_page 
)

urlpatterns = [

    # =========================
    # 🟢 FRONTEND ROUTES
    # =========================

    # Home = products list
    path('', home_page, name='home'),

    # OPTIONAL: agar /products/ bhi same page dikhana hai
    path('products/', home_page, name='products_page'),

    # ✅ PRODUCT DETAIL (IMPORTANT)
    path('product/<int:pk>/', product_detail, name='product_detail'),

    # Category page
    path('category/<slug:slug>/', category_page, name='category_page'),

    path('cart/', cart_page, name='cart_page'),


    # =========================
    # 🔵 API ROUTES
    # =========================

    path('api/products/', ProductAPI.as_view(), name='products_api'),
    path('api/products/<int:id>/', ProductAPI.as_view(), name='product_detail_api'),

    path('api/categories/', CategoryAPI.as_view(), name='categories_api'),
    path('api/categories/<int:id>/', CategoryAPI.as_view(), name='category_detail_api'),
    path('api/categories/slug/<slug:slug>/', CategoryAPI.as_view(), name='category_by_slug'),
]