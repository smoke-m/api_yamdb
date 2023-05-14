import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from reviews.models import Category, Genre, Title

CSV_FILES = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
}


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        for model, csv_file in CSV_FILES.items():
            with open(f'{settings.BASE_DIR}/static/data/{csv_file}',
                      'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                obj = [model(**data) for data in reader]
                model.objects.bulk_create(obj)
                self.stdout.write(self.style.SUCCESS(
                    f'Модель {model.__name__} загружена.'
                ))

        with open(f'{settings.BASE_DIR}/static/data/genre_title.csv',
                  'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    title = Title.objects.get(pk=row['title_id'])
                    genre = Genre.objects.get(pk=row['genre_id'])
                    title.genre.add(genre)
                except (Title.DoesNotExist, Genre.DoesNotExist) as e:
                    self.stdout.write(self.style.WARNING(f"Ошибка: {e}"))
