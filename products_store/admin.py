from django.contrib import admin
from .models import Comment
from .models import User_profile
from .models import Product
from .models import Product_type

# Register your models here.

admin.site.register(Comment)
admin.site.register(User_profile)
admin.site.register(Product)
admin.site.register(Product_type)