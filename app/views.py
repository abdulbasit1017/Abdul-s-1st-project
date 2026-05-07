from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken

# import requests
# import urllib.parse

# ❌ Google Auth removed (commented)
# from google.oauth2 import id_token
# from google.auth.transport import requests as google_requests

from .models import Product, Category, OTP
from .serializers import ProductSerializer, CategorySerializer, MyTokenSerializer
from .utils import generate_otp
from django.core.mail import send_mail


# =========================
# AUTH SYSTEM
# =========================

# class SignupView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response({"error": "Username and password required"}, status=400)

#         if User.objects.filter(username=username).exists():
#             return Response({"error": "User already exists"}, status=400)

#         user = User.objects.create(
#             username=username,
#             password=make_password(password)
#         )

#         request.session['user_id'] = user.id
#         return Response({"message": "Signup successful"})


# def signup_page(request):
#     return render(request, "signup.html")


# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get("username")
#         password = request.data.get("password")

#         if not username or not password:
#             return Response({"error": "Username and password required"}, status=400)

#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)

#         if not check_password(password, user.password):
#             return Response({"error": "Invalid password"}, status=400)

#         request.session['user_id'] = user.id
#         return Response({"message": "Login successful"})


# def login_page(request):
#     return render(request, "login.html")


# class LogoutView(APIView):
#     def post(self, request):
#         request.session.flush()
#         return Response({"message": "Logged out"})


# class UsersListView(APIView):
#     def get(self, request):
#         if not request.session.get('user_id'):
#             return Response({"error": "Login required"}, status=403)

#         users = User.objects.all().values('id', 'username')
#         return Response(users)


# class DeleteUserView(APIView):
#     def delete(self, request, id):
#         if not request.session.get('user_id'):
#             return Response({"error": "Unauthorized"}, status=403)

#         user = get_object_or_404(User, id=id)
#         user.delete()
#         return Response({"message": "User deleted"})


# class MyTokenView(TokenObtainPairView):
#     serializer_class = MyTokenSerializer


# =========================
# FRONTEND PAGES
# =========================

def home_page(request):
    categories = Category.objects.all()
    return render(request, "home.html", {"categories": categories})


def cart_page(request):
    return render(request, "cart.html")


def category_list(request):
    categories = Category.objects.all()
    return render(request, "category_list.html", {"categories": categories})


def category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)

    search = request.GET.get('search')
    if search:
        products = products.filter(name__icontains=search)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price and max_price:
        try:
            products = products.filter(
                price__gte=int(min_price),
                price__lte=int(max_price)
            )
        except ValueError:
            pass

    return render(request, "category.html", {
        "category": category,
        "products": products
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, "product_detail.html", {"product": product})


# =========================
# CATEGORY API
# =========================

class CategoryAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id=None, slug=None):

        if slug:
            category = get_object_or_404(Category, slug=slug)
            products = Product.objects.filter(category=category)

            return Response({
                "id": category.id,
                "name": category.name,
                "slug": category.slug,
                "products": [
                    {
                        "id": p.id,
                        "name": getattr(p, "name", "No Name"),
                        "price": p.price,
                        "description": p.description,
                        "image": p.image.url if p.image else ""
                    }
                    for p in products
                ]
            })

        if id:
            category = get_object_or_404(Category, id=id)
            return Response(CategorySerializer(category).data)

        categories = Category.objects.all()
        return Response(CategorySerializer(categories, many=True).data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def put(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, id):
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        category = get_object_or_404(Category, id=id)
        category.delete()
        return Response({"message": "Deleted"})


# =========================
# PRODUCT API
# =========================

class ProductAPI(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id=None):

        if id:
            product = get_object_or_404(Product, id=id)
            return Response(ProductSerializer(product).data)

        products = Product.objects.all()

        search = request.GET.get('search')
        if search:
            products = products.filter(title__icontains=search)

        return Response(ProductSerializer(products, many=True).data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def put(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, id):
        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        product = get_object_or_404(Product, id=id)
        product.delete()
        return Response({"message": "Product deleted"})


# =========================
# PRODUCT SEARCH API
# =========================

class ProductSearchAPI(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['title']


# =========================
# OTP SYSTEM
# =========================

class SendOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email required"}, status=400)

        otp = generate_otp()

        OTP.objects.filter(email=email).delete()
        OTP.objects.create(email=email, otp=otp)

        send_mail(
            'Your OTP Code',
            f'Your OTP is {otp}',
            'your_email@gmail.com',
            [email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent"})


class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            record = OTP.objects.filter(email=email, otp=otp).latest('created_at')

            if timezone.now() > record.created_at + timedelta(minutes=5):
                return Response({"error": "OTP expired"}, status=400)

            return Response({"message": "OTP verified"})

        except OTP.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=400)


# =========================
# GOOGLE AUTH (FINAL FIXED - DJANGO TEMPLATE MODE)
# =========================

# class GoogleLoginView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         base_url = "https://accounts.google.com/o/oauth2/v2/auth"

#         params = {
#             "client_id": settings.GOOGLE_CLIENT_ID,
#             "redirect_uri": settings.GOOGLE_REDIRECT_URI,
#             "response_type": "code",
#             "scope": "openid email profile",
#             "access_type": "offline",
#             "prompt": "consent"
#         }

#         return redirect(f"{base_url}?{urllib.parse.urlencode(params)}")


# class GoogleCallbackAPIView(APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         code = request.GET.get('code')

#         if not code:
#             return redirect("/?error=code_missing")

#         data = {
#             'code': code,
#             'client_id': settings.GOOGLE_CLIENT_ID,
#             'client_secret': settings.GOOGLE_CLIENT_SECRET,
#             'redirect_uri': settings.GOOGLE_REDIRECT_URI,
#             'grant_type': 'authorization_code'
#         }

#         token_response = requests.post(
#             'https://oauth2.googleapis.com/token',
#             data=data
#         )

#         if token_response.status_code != 200:
#             return redirect("/?error=token_failed")

#         token_data = token_response.json()
#         id_token_value = token_data.get('id_token')

#         if not id_token_value:
#             return redirect("/?error=no_id_token")

#         try:
#             idinfo = id_token.verify_oauth2_token(
#                 id_token_value,
#                 google_requests.Request(),
#                 settings.GOOGLE_CLIENT_ID
#             )

#             email = idinfo.get('email')

#             if not idinfo.get('email_verified'):
#                 return redirect("/?error=email_not_verified")

#             user, created = User.objects.get_or_create(username=email)
#             user.email = email
#             user.first_name = idinfo.get('given_name', '')
#             user.last_name = idinfo.get('family_name', '')
#             user.save()

#             request.session['user_id'] = user.id

#             refresh = RefreshToken.for_user(user)
#             access = str(refresh.access_token)

#             # 👉 IMPORTANT: Django template redirect
#             return redirect(f"/?access={access}")

#         except ValueError:
#             return redirect("/?error=invalid_token")