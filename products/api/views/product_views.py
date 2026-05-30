# pyrefly: ignore [missing-import]
from rest_framework import generics
from products.models import Product
from ..serializers.product_serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(in_stock=True)
        category_slug = self.request.query_params.get('category_slug')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset

    