from django.conf import settings
# pyrefly: ignore [missing-import]
from enum import unique
# pyrefly: ignore [missing-import]
from django.db import models
from .category import Category
from django.db.models import Avg

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=225, db_index=True)
    slug = models.SlugField(max_length=225, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/products/%Y/%m/%d', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=50, unique=True)
    in_stock = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_average_rating(self):
        average = self.reviews.aggregate(Avg('rating'))['rating__avg']
        return average if average else 0

    class Meta:
        verbose_name_plural = 'products'
        ordering = ('-created',)

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d')
    alt_text = models.CharField(max_length=225, blank=True, null=True)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
        

class Attribute(models.Model):
    name = models.CharField(max_length=225)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(Attribute, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=225)

    def __str__(self):
        return f"{self.attribute.name}:{self.value}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, related_name = 'variants', on_delete=models.CASCADE)
    attribute_values = models.ManyToManyField(AttributeValue, related_name='variants')
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.product.name} - {self.sku}"
        
class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) 
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'user')

    def __str__(self):
        return f"{self.user.email} - {self.product.name} - {self.rating} Stars"
