from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

# Create your models here.

class Comment(models.Model):
    comname = models.CharField(max_length=100)
    comtext = models.TextField()
    commented_date = models.DateTimeField(default=timezone.now)
    comwriter = models.ForeignKey(User, on_delete=models.CASCADE)