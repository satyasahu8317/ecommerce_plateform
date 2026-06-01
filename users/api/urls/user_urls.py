from django.urls import path
from ..views.user_views import CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
]