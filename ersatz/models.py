from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    nutrition_grades = models.CharField(max_length=1)
    code = models.CharField(max_length=13, unique=True)
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
