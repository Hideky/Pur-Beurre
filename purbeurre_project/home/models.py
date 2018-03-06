from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200)
    id_off = models.IntegerField()
    brands = models.CharField(max_length=200)
    nutrition_grade = models.CharField(max_length=1)
    satured_fat = models.FloatField()
    fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    categorie = models.CharField(max_length=100)
    img_url = models.URLField()
    url = models.URLField()

class UserInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Product, related_name='favorited', blank=True)