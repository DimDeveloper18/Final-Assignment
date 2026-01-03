from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary_storage.storage import MediaCloudinaryStorage

User = get_user_model()

# Create your models here.

class Comment(models.Model):
    comname = models.CharField(max_length=100)
    comtext = models.TextField()
    commented_date = models.DateTimeField(default=timezone.now)
    comwriter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comname
    
    def get_absolute_url(self):
        return reverse('products_store-comment-detail', kwargs={"pk": self.pk})
    
class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='profile_pics/')

    def __str__(self):
        return f'{self.user.username} User_profile'
    
class Prod_type(models.Model):
    prod_type_name = models.CharField(max_length=25)

    def __str__(self):
        return self.prod_type_name
    
class Product(models.Model):
    prod_name = models.CharField(max_length=50)
    prod_brand = models.CharField(max_length=25)
    prod_model = models.CharField(max_length=25)
    prod_id_name = models.IntegerField(max_length=0)
    prod_stock = models.CharField(max_length=20, unique=True)
    stock_date = models.DateTimeField(auto_now_add=True)
    prod_price = models.DecimalField(max_digits=10, decimal_places=2)
    prod_type = models.ForeignKey(Prod_type, on_delete=models.RESTRICT, null=True)
    
    def __str__(self):
        return self.prod_name

