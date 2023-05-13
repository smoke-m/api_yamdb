from django.db import models

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
    year = models.IntegerField()
    description = models.CharField(blank=True, null=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name[:40]
