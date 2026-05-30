
# pyrefly: ignore [missing-import]
from django.contrib.postgres.search import SearchVector
# pyrefly: ignore [missing-import]
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend   
from products.models import Product
from ..serializers.product_serializers import ProductSerializer
from ..filters.product_filters import ProductFilter

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(in_stock=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter 
 
    def get_queryset(self):
        # 1. Base Queryset
        queryset = Product.objects.filter(in_stock=True)
        
        # 2. Add Search Logic (django-filter doesn't do this part)
        query = self.request.query_params.get('search')
        if query:
            queryset = queryset.annotate(
                search=SearchVector('name', 'description'),
            ).filter(search=query)
            
        # 3. Hand everything else to the Filters
        return queryset
   