from rest_framework import viewsets, permissions
from ..models import Address
from .serializers import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Production Pattern: Never return data belonging to other users
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically link the address to the logged-in user
        serializer.save(user=self.request.user)
