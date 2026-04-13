from rest_framework import serializers
from .models import Product, Category


class ProductSerializer(serializers.ModelSerializer):

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long")

        if len(value) > 50:
            raise serializers.ValidationError("Name must not exceed 50 characters")

        return value

    class Meta:
        model = Product
        fields = '__all__'


# ✅ YE ALAG CLASS HONA CHAHIYE (IMPORTANT)
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'