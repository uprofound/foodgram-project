import csv
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient  # isort:skip


class Command(BaseCommand):
    help = 'Load ingredients data from csv-file to DB.'

    def handle(self, *args, **options):
        with open(
                os.path.join('recipes', 'data', 'ingredients.csv'),
                encoding='utf-8'
        ) as f:
            reader = csv.reader(f)
            for row in reader:
                name, measurement_unit = row
                Ingredient.objects.get_or_create(
                    name=name,
                    measurement_unit=measurement_unit
                )
