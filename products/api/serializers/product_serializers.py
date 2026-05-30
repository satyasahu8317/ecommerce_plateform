# pyrefly: ignore [missing-import]
from rest_framework import serializers
from products.models import Product, Category   

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'slug', 'description', 'price', 'in_stock', 'average_rating']

    def get_average_rating(self, obj):
        return obj.get_average_rating()
        