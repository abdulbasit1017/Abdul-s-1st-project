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
# 🟢 AUTH APIS
# =========================

class SignupView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"error": "User already exists"}, status=400)

        User.objects.create(
            username=username,
            password=make_password(password)
        )

        return Response({"message": "User created successfully"})


class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            request.session['user_id'] = user.id
            return Response({"message": "Login successful"})

        return Response({"error": "Invalid credentials"}, status=400)


class LogoutView(APIView):
    def post(self, request):
        request.session.flush()
        return Response({"message": "Logged out"})


class UsersListView(APIView):
    def get(self, request):
        if not request.session.get('user_id'):
            return Response({"error": "Login required"}, status=403)

        users = User.objects.all().values('id', 'username')
        return Response(users)


class DeleteUserView(APIView):
    def delete(self, request, id):
        user = get_object_or_404(User, id=id)
        user.delete()
        return Response({"message": "User deleted"})


# =========================
# 🟢 FRONTEND VIEWS
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
# 🟢 CATEGORY API (FIXED 🔥)
# =========================

class CategoryAPI(APIView):

    def get(self, request, id=None, slug=None):

        # Single category with products (IMPORTANT FIX)
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
                        "name": getattr(p, "name", getattr(p, "title", "No Name")),
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
# 🟡 PRODUCT API
# =========================

class ProductAPI(APIView):

    def get(self, request, id=None):

        if id:
            product = get_object_or_404(Product, id=id)
            return Response(ProductSerializer(product).data)

        products = Product.objects.all()

        category_id = request.GET.get('category')
        category_slug = request.GET.get('category_slug')
        search = request.GET.get('search')

        if category_id:
            products = products.filter(category_id=category_id)

        if category_slug:
            products = products.filter(category__slug=category_slug)

        if search:
            products = products.filter(name__icontains=search)

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