from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return '{}, {}'.format(self.name, self.measurement_unit)
