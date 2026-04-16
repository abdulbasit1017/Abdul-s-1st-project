from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer

# =========================
# 🟢 For Signup
# =========================
class SignupView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password both are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User.objects.create(
            username=username,
            password=make_password(password)  # 🔐 password hashed
        )

        return Response({"message": "User created successfully"})
    
# =========================
# 🟢 For Login
# =========================

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            request.session['user_id'] = user.id
            return Response({"message": "Login successful"})
        else:
            return Response({"error": "Invalid credentials"}, status=400)
        
        
# =========================
# 🟢 For Logout
# =========================
        
class LogoutView(APIView):
    def post(self, request):
        request.session.flush()
        return Response({"message": "Logged out successfully"})
    
# ==========================
# 🟢 For Checking UserLists
# ==========================

class UsersListView(APIView):
    def get(self, request):
        if not request.session.get('user_id'):
            return Response({"error": "Login required"}, status=403)
        users = User.objects.all().values('id', 'username')
        return Response(users)
    
    

# ========================
# 🟢 For Deletion
# ========================

class DeleteUserView(APIView):
    def delete(self, request, id):
        user = User.objects.get(id=id)
        user.delete()
        return Response({"message": "User deleted"})

        

# =========================
# 🟢 FRONTEND VIEWS
# =========================
def cart_page(request):
    return render(request, "cart.html")
# 🏠 HOME PAGE (CATEGORIES SHOW)
def home_page(request):
    categories = Category.objects.all()
    return render(request, "home.html", {'categories': categories})


# 📦 CATEGORY PAGE (FILTER PRODUCTS BY SLUG)
def category_page(request, slug):
    category = get_object_or_404(Category, slug=slug)

    products = Product.objects.filter(category=category)

    # 🔍 SEARCH
    search = request.GET.get('search')
    if search:
        products = products.filter(title__icontains=search)

    # 💰 PRICE FILTER
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
        'category': category,
        'products': products
    })


# 🔥 PRODUCT DETAIL PAGE (FIXED)
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, "product_detail.html", {"product": product})


# =========================
# 🟢 CATEGORY API
# =========================
class CategoryAPI(APIView):

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None, slug=None):

        if id is not None:
            category = get_object_or_404(Category, id=id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        if slug is not None:
            category = get_object_or_404(Category, slug=slug)
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def put(self, request, id=None):
        if id is None:
            return Response({'error': 'Category ID required'}, status=400)

        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def patch(self, request, id=None):
        if id is None:
            return Response({'error': 'Category ID required'}, status=400)

        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        if id is None:
            return Response({'error': 'Category ID required'}, status=400)

        category = get_object_or_404(Category, id=id)
        category.delete()

        return Response(
            {'message': 'Category deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )


# =========================
# 🟡 PRODUCT API
# =========================
class ProductAPI(APIView):

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, id=None):

        if id is not None:
            product = get_object_or_404(Product, id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)

        category_id = request.GET.get('category')
        category_slug = request.GET.get('category_slug')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        search = request.GET.get('search')

        products = Product.objects.all()

        if category_id:
            products = products.filter(category_id=category_id)

        if category_slug:
            products = products.filter(category__slug=category_slug)

        if min_price and max_price:
            try:
                products = products.filter(
                    price__gte=int(min_price),
                    price__lte=int(max_price)
                )
            except ValueError:
                return Response({'error': 'Invalid price range'}, status=400)

        if search:
            products = products.filter(title__icontains=search)

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def put(self, request, id=None):
        if id is None:
            return Response({'error': 'Product ID required'}, status=400)

        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def patch(self, request, id=None):
        if id is None:
            return Response({'error': 'Product ID required'}, status=400)

        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        if id is None:
            return Response({'error': 'Product ID required'}, status=400)

        product = get_object_or_404(Product, id=id)
        product.delete()

        return Response(
            {'message': 'Product deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )