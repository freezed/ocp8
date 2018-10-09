from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    nutrition_grades = models.CharField(max_length=1)
    nova_group = models.CharField(max_length=1)
    code = models.CharField(max_length=13, unique=True)
    category = models.ManyToManyField(Category, related_name='products', blank=True)

    def __str__(self):
        return self.name
