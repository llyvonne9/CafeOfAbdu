from django.db import models

# Create your models here.
class Dish(models.Model):
    name = models.CharField(max_length=100)
    like = models.CharField(max_length=100,default="")
