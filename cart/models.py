from django.db import models
from django.conf import settings
from products.models import Product, ProductVariant


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart: {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name =  'items', on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity=models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} X {self.product.name}"

    def get_total_price(self):
        # Use variant price if available, otherwise use base product price
        price = self.variant.price if self.variant and self.variant.price else self.product.price 
        return price*self.quantity