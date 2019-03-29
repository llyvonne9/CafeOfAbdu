from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=100)
    location = models.TextField()
    url = models.TextField()
    phone = models.CharField(max_length=50)
    likes = models.IntegerField(default=1)
