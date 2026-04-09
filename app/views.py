from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product

class ProductAPI(APIView):
    
    # POST: Create a new product
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # GET: Retrieve product(s)
    # - By ID: /products/<id>/
    # - By price range: /products/?min_price=10&max_price=50
    # - All products: /products/
    def get(self, request, id=None):
        # 1️⃣ Get by ID
        if id is not None:
            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=404)
            serializer = ProductSerializer(product)
            return Response(serializer.data)
        
        # 2️⃣ Get by price range
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        if min_price is not None and max_price is not None:
            try:
                min_price = float(min_price)
                max_price = float(max_price)
            except ValueError:
                return Response({'error': 'Invalid price range'}, status=400)
            
            products = Product.objects.filter(price__gte=min_price, price__lte=max_price)
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        
        # 3️⃣ Otherwise return all products
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    # PUT: Update an existing product
    # URL: /products/<id>/
    def put(self, request, id=None):
        # Make sure ID is provided
        if id is not None:
            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                return Response({'error': 'Product not found'}, status=404)
            
            # Update product
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
            # If ID is missing
        return Response({'error': 'Product ID required for update'}, status=400)
    
    # For Patch
    def patch(self,request,id=None):
        if id is not None:
            try:
                product=Product.objects.get(id=id)
            except Product.DoesNotExist:
                return Response ({'error':'Product not found'}, status=404)
            
            serializer = ProductSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response (serializer.data)
            return Response (serializer.errors, status=400)
        
        return Response({'error': 'Product ID required for patch'}, status=400)

        
    