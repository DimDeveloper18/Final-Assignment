from django.contrib import admin
from .models import Comment, User_profile, Product, Product_type, Product_subtype

# Register your models here.

admin.site.register(Comment)
admin.site.register(User_profile)
admin.site.register(Product)
admin.site.register(Product_type)
admin.site.register(Product_subtype)