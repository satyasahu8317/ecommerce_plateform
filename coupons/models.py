from django.db import models

# Create your models here.
from django.core.validators import MinValueValidator, MaxValueValidator

class Coupon(models.Model):
    # The two type of discounts
    DISCOUNT_CHOICES = (
        ('percentage','Percentage(%)'),
        ('flat','Flat Amount(Rs)'),
    )
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # Expiry Logic
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} ({self.amount} {self.discount_type})"

    def is_valid(self):
        # pyrefly: ignore [missing-import]
        from django.utils import timezone
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to