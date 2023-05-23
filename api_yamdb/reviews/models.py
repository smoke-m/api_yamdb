from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import max_min_validator, validate_username, validate_year


class User(AbstractUser):
    """Модель юзера."""
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE = [
        (USER, 'пользователь'),
        (MODERATOR, 'модератор'),
        (ADMIN, 'админ'),
    ]
    username = models.CharField(
        max_length=settings.USERNAME_LENGTH, unique=True,
        validators=(validate_username,
                    UnicodeUsernameValidator(regex=(r'^[\w.@+-]+\Z')))
    )
    last_name = models.CharField(
        max_length=settings.LAST_NAME_LENGTH, blank=True)
    first_name = models.CharField(
        max_length=settings.FIRST_NAME_LENGTH, blank=True)
    email = models.EmailField(max_length=settings.EMAIL_LENGTH, unique=True,
                              blank=False, null=False)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=settings.ROLE_LENGTH,
                            choices=ROLE, default=USER)

    class Meta:
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email',
            )
        ]

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    def __str__(self):
        return f'{self.username} {self.email} {self.role}'


class BaseModelGenreCategory(models.Model):
    """Базовая модель для: Genre, Category."""
    name = models.CharField(max_length=settings.NAME_LENGTH)
    slug = models.SlugField(max_length=settings.SLAG_LENGTH, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Genre(BaseModelGenreCategory):
    """Модель Genre."""
    class Meta:
        ordering = ['-id']


class Category(BaseModelGenreCategory):
    """Модель Category."""
    class Meta:
        ordering = ['-id']


class Title(models.Model):
    """Модель Title."""
    name = models.CharField(max_length=settings.NAME_LENGTH)
    year = models.PositiveSmallIntegerField(validators=[validate_year])
    description = models.CharField(
        max_length=settings.DESCRIPTION_LENGTH, blank=True)
    genre = models.ManyToManyField(Genre, related_name='titles')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='titles')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class BaseModelCommentReview(models.Model):
    """Базовая модель для: Comment, Review."""
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.text


class Review(BaseModelCommentReview):
    """Модель отзывов с оценкой на произведение."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=max_min_validator()
    )

    class Meta:
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]
        ordering = ['-id']


class Comment(BaseModelCommentReview):
    """Модель комментариев к отзывам."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
    )

    class Meta:
        default_related_name = 'comments'
        ordering = ['-id']
