from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from cloudinary_storage.storage import MediaCloudinaryStorage

# Create your models here.

class Comment(models.Model):
    comname = models.CharField(max_length=100)
    comtext = models.TextField()
    commented_date = models.DateTimeField(default=timezone.now)
    comwriter = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comname
    
class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(storage=MediaCloudinaryStorage(), upload_to='profile_pics/')

    def __str__(self):
        return f'{self.user.username} User_profile'
