from django.conf import settings
from django.db import models

class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='addresses', 
        on_delete=models.CASCADE
    )
    # Contact Info
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    
    # Geography
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    # Meta
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def save(self, *args, **kwargs):
        """
        Production Pattern: Automatic Default Management
        If this address is saved as default, we must ensure 
        all other addresses for this user are NOT default.
        """
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.city}"
