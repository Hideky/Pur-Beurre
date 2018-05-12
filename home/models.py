from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
    """Product model created with OFFData's return data"""
    name = models.CharField(max_length=200)
    id_off = models.BigIntegerField()
    brands = models.CharField(max_length=200)
    nutrition_grade = models.CharField(max_length=1)
    satured_fat = models.FloatField()
    fat = models.FloatField()
    sugar = models.FloatField()
    salt = models.FloatField()
    categorie = models.CharField(max_length=100)
    img_url = models.URLField()
    url = models.URLField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "produit"


class Profile(models.Model):
    """Proile model extending the default User model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorites = models.ManyToManyField(Product, related_name='favorited', blank=True)
    api_token = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a Profile model when a User model was created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Edit a Profile model when a User model was edited"""
    instance.profile.save()
