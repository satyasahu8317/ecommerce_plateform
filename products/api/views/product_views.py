# pyrefly: ignore [missing-import]
from django.contrib.postgres.search import SearchVector
# pyrefly: ignore [missing-import]
from rest_framework import generics
from products.models import Product
from ..serializers.product_serializers import ProductSerializer

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(in_stock=True)
        query = self.request.query_params.get('search')
        if query:
            queryset = queryset.annotate(
                search=SearchVector('name', 'description'),
            ).filter(search=query)

        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)    
        
        return queryset

    