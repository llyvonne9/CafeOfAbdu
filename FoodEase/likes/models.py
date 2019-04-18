from django.db import models
from django.contrib.auth.models import User
from restaurant import models as restaurant_models

# Create your models here.
class Likes(models.Model):
    rest_id = models.ForeignKey(restaurant_models.Restaurant, on_delete = models.CASCADE)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE)
    count = models.IntegerField(default=1)
