from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    ProductAPI, CategoryAPI,

    # FRONTEND
    home_page, category_page, category_list,
    product_detail, cart_page,
    signup_page,login_page,

    # AUTH APIs
    SignupView, LoginView, LogoutView,
    UsersListView, DeleteUserView,

    # OTP
    SendOTPView, VerifyOTPView,

    # JWT
    MyTokenView,
)

urlpatterns = [

    # =========================
    # 🟢 FRONTEND ROUTES
    # =========================

    path('', home_page, name='home'),

    path('signup/', signup_page),
    path('login/', login_page),
    path('api/login/', LoginView.as_view()), 

    path('products/', home_page, name='products_page'),

    path('product/<int:pk>/', product_detail, name='product_detail'),

    path('categories/', category_list, name='category_list'),

    path('category/<slug:slug>/', category_page, name='category_page'),

    path('cart/', cart_page, name='cart_page'),


    # =========================
    # 🔵 AUTH API ROUTES
    # =========================

    path('api/signup/', SignupView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),

    path('api/users/', UsersListView.as_view()),
    path('api/users/<int:id>/', DeleteUserView.as_view()),


    # =========================
    # 🟡 OTP ROUTES
    # =========================

    path('api/send-otp/', SendOTPView.as_view()),
    path('api/verify-otp/', VerifyOTPView.as_view()),


    # =========================
    # 🟣 PRODUCT API
    # =========================

    path('api/products/', ProductAPI.as_view()),
    path('api/products/<int:id>/', ProductAPI.as_view()),


    # =========================
    # 🟠 CATEGORY API
    # =========================

    path('api/categories/', CategoryAPI.as_view()),
    path('api/categories/<int:id>/', CategoryAPI.as_view()),
    path('api/categories/slug/<slug:slug>/', CategoryAPI.as_view()),


    # =========================
    # 🔐 JWT AUTH (OPTIONAL)
    # =========================

    path('api/token/', MyTokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]