from django.db import models
from accounts.models import CustomUser
from django.utils import timezone
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# Model Product
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(blank=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False)
    image = models.ImageField(upload_to='products/', blank=True)
    date_added = models.DateTimeField(default=timezone.now)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-date_added']

    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        # Retourne l'URL de votre image par défaut
        return settings.STATIC_URL + 'images/default-image.webp'

class Cart(models.Model):
    user = models.OneToOneField(CustomUser, related_name='cart', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.username}"
    
    def get_cart_total(self):
        items = self.items.all()
        return sum(item.get_total() for item in items)

    def get_cart_items_total(self):
        items = self.items.all()
        return sum(item.quantity for item in items)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"
    
    def get_total(self):
        return self.quantity * self.product.price
    

class AddressShipping(models.Model):
    user = models.ForeignKey(CustomUser, related_name='shipping_addresses', on_delete=models.CASCADE)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}'s address"
