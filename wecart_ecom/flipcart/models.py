from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
class Category(models.Model):
    cname=models.CharField(max_length=100)
    image=models.ImageField(upload_to="image/")
    def __str__(self):
        return self.cname
class Products(models.Model):
    title=models.CharField(max_length=100)
    desc=models.TextField()
    price=models.IntegerField()
    image=models.ImageField(upload_to="image/")
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):
        return self.title
class AddCart(models.Model):
    products=models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.products.title}-{self.quantity}'
class Profile(models.Model):
    name=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    def __str__(self):
        return self.name.username
class I(models.Model):
    image=models.ImageField(upload_to='image/')
class Payment(models.Model):
    payment_method=models.CharField(max_length=100)
    
    def __str__(self):
        return self.payment_method

class Buynow(models.Model):
    payment=models.ForeignKey(Payment,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    products=models.ForeignKey(Products,on_delete=models.CASCADE)
    total=models.IntegerField()
    delivary_date=models.DateField(default=timezone.now)
    def __str__(self):
        return f"{self.products.title}- {self.payment.payment_method} - {self.total}"
class Banner(models.Model):
    title=models.CharField(max_length=100)
    desc=models.TextField()
    image=models.ImageField(upload_to='image/')
    def __str__(self):
        return self.title