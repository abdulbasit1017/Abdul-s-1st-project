from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


# =========================
# 🟢 CATEGORY API
# =========================
class CategoryAPI(APIView):

    # CREATE CATEGORY
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET ALL / SINGLE CATEGORY
    def get(self, request, id=None):

        if id is not None:
            category = get_object_or_404(Category, id=id)
            serializer = CategorySerializer(category)
            return Response(serializer.data)

        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    # UPDATE FULL CATEGORY
    def put(self, request, id=None):
        if id is None:
            return Response({'error': 'Category ID required'}, status=400)

        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # PARTIAL UPDATE CATEGORY
    def patch(self, request, id=None):
        if id is None:
            return Response({'error': 'Category ID required'}, status=400)

        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(category, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # DELETE CATEGORY
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

    # CREATE PRODUCT
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET PRODUCTS (ALL / SINGLE / FILTER)
    def get(self, request, id=None):

        # SINGLE PRODUCT
        if id is not None:
            product = get_object_or_404(Product, id=id)
            serializer = ProductSerializer(product)
            return Response(serializer.data)

        # 🔥 CATEGORY FILTER
        category_id = request.GET.get('category')
        if category_id:
            products = Product.objects.filter(category_id=category_id)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

        # PRICE FILTER
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        if min_price and max_price:
            try:
                min_price = int(min_price)
                max_price = int(max_price)
            except ValueError:
                return Response({'error': 'Invalid price range'}, status=400)

            products = Product.objects.filter(
                price__gte=min_price,
                price__lte=max_price
            )
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)

        # ALL PRODUCTS
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # UPDATE FULL PRODUCT
    def put(self, request, id=None):
        if id is None:
            return Response({'error': 'Product ID required'}, status=400)

        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # PARTIAL UPDATE PRODUCT
    def patch(self, request, id=None):
        if id is None:
            return Response({'error': 'Product ID required'}, status=400)

        product = get_object_or_404(Product, id=id)
        serializer = ProductSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)

    # DELETE PRODUCT
    def delete(self, request, id=None):
        if id is None:
            return Response({'error': 'Product ID required'}, status=400)

        product = get_object_or_404(Product, id=id)
        product.delete()

        return Response(
            {'message': 'Product deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )