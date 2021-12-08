from colorfield.fields import ColorField
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = ColorField(default='#32cd32', unique=True)  # Lime Green
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name
