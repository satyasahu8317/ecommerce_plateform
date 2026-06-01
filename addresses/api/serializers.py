from rest_framework import serializers
from ..models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'id', 'full_name', 'phone_number', 
            'street_address', 'city', 'postal_code', 'is_default'
        ]
        read_only_fields = ['id']
