from django.db import models
from restaurant import models as restaurant_models
from dish import models as dish_models

# Create your models here.

class Serves(models.Model):
    restaurant_id = models.ForeignKey(restaurant_models.Restaurant, on_delete = models.CASCADE)
    dish_id = models.ForeignKey(dish_models.Dish, on_delete = models.CASCADE)
    ave_rating = models.FloatField(default=0.0)
    ave_wait = models.FloatField(default=0.0)
    is_speciality = models.BooleanField()
    is_veg = models.BooleanField()
    price = models.FloatField()
