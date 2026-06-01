from django.db import models
from django.conf import settings
from products.models import Product, ProductVariant
from addresses.models import Address

class Order(models.Model):
    class Status(models.TextChoices):
        """Production Pattern: Named choices for type-safety and readability"""
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        SHIPPED = 'SHIPPED', 'Shipped'
        DELIVERED = 'DELIVERED', 'Delivered'
        CANCELLED = 'CANCELLED', 'Cancelled'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='orders'
    )

    # 1. THE CONNECTION: Link to the reusable address book
    shipping_address = models.ForeignKey(
        Address, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='orders'
    )

    # 2. THE SNAPSHOT: Frozen address data for historical integrity
    # We populate these during checkout so the order record survives if the 
    # user later deletes their address from the address book.
    full_name_snapshot = models.CharField(max_length=150, blank=True)
    email_snapshot = models.EmailField(blank=True)
    phone_snapshot = models.CharField(max_length=20, blank=True)
    address_snapshot = models.TextField(blank=True)
    city_snapshot = models.CharField(max_length=100, blank=True)
    postal_code_snapshot = models.CharField(max_length=20, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20, 
        choices=Status.choices, 
        default=Status.PENDING
    )
    total_paid = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    # 3. PRODUCTION PATTERN: Transition Methods
    # These ensure that business logic is followed when changing states.
    def confirm_order(self):
        if self.status == self.Status.PENDING:
            self.status = self.Status.CONFIRMED
            self.save()
            return True
        return False

    def ship_order(self):
        if self.status == self.Status.CONFIRMED:
            self.status = self.Status.SHIPPED
            self.save()
            # This is where a tracking number would be generated
            return True
        return False


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.SET_NULL)

    # We save the price at the time of purchase (Snapshot)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Item {self.id} for Order {self.order.id}"

    def get_total_item_price(self):
        return self.price * self.quantity
