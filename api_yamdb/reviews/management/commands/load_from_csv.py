import csv
from pathlib import Path

from django.core.management.base import BaseCommand
from django.db import transaction

from reviews.models import Category, Comment, Genre, Review, Title, User

CSV_PATH = Path('static', 'data')

CSV_FILES = (
    ('category.csv', Category, {}),
    ('genre.csv', Genre, {}),
    ('users.csv', User, {}),
    ('titles.csv', Title, {'category': 'category_id'}),
    ('genre_title.csv', Title.genre.through, {}),
    ('review.csv', Review, {'author': 'author_id'}),
    ('comments.csv', Comment, {'author': 'author_id'}),
)


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **kwargs):

        for file, model, replace in CSV_FILES:
            try:
                with open(Path(CSV_PATH, file), mode='r', encoding='utf8') as f:
                    reader = csv.DictReader(f)
                    obj = []
                    for row in reader:
                        args = dict(**row)
                        if replace:
                            for old, new in replace.items():
                                args[new] = args.pop(old)
                        obj.append(model(**args))
                    model.objects.bulk_create(obj)
                    self.stdout.write(self.style.SUCCESS(
                        f'Модель {model.__name__} загружена.'
                    ))
            except Exception as error:
                self.stdout.write(self.style.ERROR(
                    f'Ошибка при обработке {file}: {error}'
                ))
