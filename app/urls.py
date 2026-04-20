from django.urls import path
from .views import (
    ProductAPI, CategoryAPI,
    home_page, category_page, category_list,
    product_detail, cart_page,
    SignupView, LoginView, LogoutView,
    UsersListView, DeleteUserView
)

urlpatterns = [

    # =========================
    # 🟢 FRONTEND ROUTES
    # =========================

    path('', home_page, name='home'),
    path('products/', home_page, name='products_page'),

    path('product/<int:pk>/', product_detail, name='product_detail'),

    path('categories/', category_list, name='category_list'),
    path('category/<slug:slug>/', category_page, name='category_page'),

    path('cart/', cart_page, name='cart_page'),

    # =========================
    # 🔵 API ROUTES
    # =========================

    path('api/signup/', SignupView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),

    path('api/users/', UsersListView.as_view()),
    path('api/users/<int:id>/', DeleteUserView.as_view()),

    path('api/products/', ProductAPI.as_view()),
    path('api/products/<int:id>/', ProductAPI.as_view()),

    path('api/categories/', CategoryAPI.as_view()),
    path('api/categories/<int:id>/', CategoryAPI.as_view()),
    path('api/categories/slug/<slug:slug>/', CategoryAPI.as_view()),
]