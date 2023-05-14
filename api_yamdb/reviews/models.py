from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_year

User = get_user_model()
# Пока не создали полноценную модель))


class Genre(models.Model):
    """Модель Genre."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name[:40]


class Category(models.Model):
    """Модель Category."""
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name[:40]


class Title(models.Model):
    """Модель Title."""
    name = models.CharField(max_length=256)
    year = models.IntegerField(validators=[validate_year])
    description = models.CharField(max_length=1024, blank=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 related_name='titles')

    class Meta:
        ordering = ['year']

    def __str__(self):
        return self.name[:40]
