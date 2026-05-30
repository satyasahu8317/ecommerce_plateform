from django.urls import path
from ..views.product_views import ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
]