from django.contrib import admin

# Register your models here.
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        'code',
        'discount_type',
        'amount',
        'valid_to',
        'active',
    ]
    
    list_filter = [
        'active',
        'discount_type',
    ]
    search_fields = [
        'code',
    ]