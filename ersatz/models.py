from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Most attributes are original OpenFF API `product field`
    Other are specific fields processed , see @staticmethod in
    ersatz.view.toolbox.SearchProduct to process this fields
    """
    # Originals
    nutrition_grades = models.CharField(max_length=1)
    code = models.CharField(max_length=13, unique=True)
    url = models.CharField(max_length=255)
    ingredients_text = models.CharField(max_length=255)
    image_front_thumb_url = models.CharField(max_length=255)
    image_front_url = models.CharField(max_length=255)
    image_nutrition_url = models.CharField(
        default='https://via.placeholder.com/250x100?text=Fiche+OFF+incomplete',
        max_length=255
    )

    # Specials
    name = models.CharField(max_length=200)
    category = models.ManyToManyField(Category, related_name='products')

    def __str__(self):
        return self.name


class Favorite(models.Model):
    users = models.ForeignKey(
        User,
        related_name='favorites_user',
        on_delete=models.CASCADE,
    )
    products = models.ForeignKey(
        Product,
        related_name='favorites_product',
        on_delete=models.CASCADE,
    )
    substitutes = models.ForeignKey(
        Product,
        related_name='favorites_substitute',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "Favorite #{}".format(self.id)
