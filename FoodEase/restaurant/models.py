from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    cuisine = models.CharField(max_length=100)
    location = models.TextField()
    url = models.TextField()
    phone = models.CharField(max_length=50)
    num_likes = models.IntegerField(default=1)
    is_veg = models.BooleanField(default=False)
    is_dessert = models.BooleanField(default=False)
    is_nightlife = models.BooleanField(default=False)
    is_finedining = models.BooleanField(default=False)
    is_cafe = models.BooleanField(default=False)
