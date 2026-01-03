from django.contrib import admin
from .models import Comment
from .models import User_profile
from .models import Product
from .models import Prod_type

# Register your models here.

admin.site.register(Comment)
admin.site.register(User_profile)
admin.site.register(Product)
admin.site.register(Prod_type)