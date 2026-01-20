from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from cloudinary_storage.storage import MediaCloudinaryStorage
from cloudinary.utils import cloudinary_url
from django.templatetags.static import static

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
    
class Product_type(models.Model):
    prod_type_name = models.CharField(max_length=25)

    def __str__(self):
        return self.prod_type_name
    
class Product(models.Model):
    prod_name = models.CharField(max_length=50)
    prod_brand = models.CharField(max_length=25)
    prod_model = models.CharField(max_length=25)
    prod_id_name = models.CharField(max_length=100)
    prod_stock = models.CharField(max_length=20, unique=True)
    stock_date = models.DateTimeField(auto_now_add=True)
    prod_price = models.DecimalField(max_digits=10, decimal_places=2)
    prod_type = models.ForeignKey(Product_type, on_delete=models.CASCADE, related_name="products")
    image = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='product_pics/', null=True, blank=True)
    
    def __str__(self):
        return self.prod_name
    
    def get_image_url(self):
        if self.image:
            return cloudinary_url(
                self.image.name, 
                width=200, 
                height=100, 
                crop="scale"
            )[0]
        else:
            return static('products_store/proddefault.jpg')
    
class Product_stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    new_com = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.prod_name} - {self.quantity}"

class Product_restock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    restock = models.IntegerField()
    stock_date = models.DateTimeField(auto_now_add=True)
    prod_status = models.CharField(max_length=25)

class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Basket of {self.user.username}"
    
    def total_price(self):
        return sum(item.product.prod_price * item.quantity for item in self.items.all())
    
class Product_order(models.Model):
    order = models.ForeignKey(Basket, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.prod_name} ({self.quantity})"

