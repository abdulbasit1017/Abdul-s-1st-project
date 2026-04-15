from django.urls import path
from .views import ProductAPI, CategoryAPI, home_page, category_page

urlpatterns = [

    # =========================
    # 🟢 FRONTEND ROUTES
    # =========================
    path('', home_page, name='home'),

    # 🔥 Category frontend page (HTML)
    path('category/<slug:slug>/', category_page, name='category_page'),

    # =========================
    # 🟡 PRODUCT API
    # =========================
    path('products/', ProductAPI.as_view(), name='products'),
    path('products/<int:id>/', ProductAPI.as_view(), name='product-detail'),

    # =========================
    # 🟢 CATEGORY API
    # =========================
    path('categories/', CategoryAPI.as_view(), name='categories'),
    path('categories/<int:id>/', CategoryAPI.as_view(), name='category-detail'),

    # 🔥 CATEGORY BY SLUG (API)
    path('categories/slug/<slug:slug>/', CategoryAPI.as_view(), name='category-by-slug'),
]