from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField  # ✅ Import this

# Category model
class Category(models.Model):
    cname = models.CharField(max_length=100)
    images = CloudinaryField('image')  # ✅ Cloudinary field

    def __str__(self):
        return self.cname

# Products model
class Products(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.IntegerField()
    images = CloudinaryField('image')  # ✅ Cloudinary field
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Add to cart model
class AddCart(models.Model):
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.products.title} - {self.quantity}'

# User profile model
class Profile(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name.username

# Image model (generic)
class I(models.Model):
    images = CloudinaryField('image')  # ✅ Cloudinary field

# Payment method model
class Payment(models.Model):
    payment_method = models.CharField(max_length=100)

    def __str__(self):
        return self.payment_method

# Buy now model
class Buynow(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    total = models.IntegerField()
    delivary_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.products.title} - {self.payment.payment_method} - {self.total}"

# Banner model
class Banner(models.Model):
    title = models.CharField(max_length=100)
    desc = models.TextField()
    images = CloudinaryField('image')  # ✅ Cloudinary field

    def __str__(self):
        return self.title
