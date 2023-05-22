from django.conf import settings
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title, User
from reviews.validators import (max_min_validator, validate_username,
                                validate_year)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализер модели Genre."""
    class Meta:
        model = Genre
        fields = ['name', 'slug']
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    """Сериализер модели Category."""
    class Meta:
        model = Category
        fields = ['name', 'slug']
        lookup_field = 'slug'


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериализер модели Title(Read)."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(
        source='reviews__score__avg', read_only=True)

    class Meta:
        model = Title
        fields = ['id', 'name', 'year', 'rating',
                  'description', 'genre', 'category']


class TitleSerializerWrite(serializers.ModelSerializer):
    """Сериализер модели Title(Write)."""
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all())
    year = serializers.IntegerField(validators=[validate_year])

    class Meta:
        fields = ['id', 'name', 'year', 'description', 'genre', 'category']
        model = Title


class TokenSerializer(serializers.Serializer):
    """Сериализер отправки токена."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыввов."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    score = serializers.IntegerField(validators=max_min_validator())

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        read_only = ['id']

    def validate(self, data):
        request = self.context['request']
        title = self.context['view'].kwargs.get('title_id')
        if request.method == 'POST':
            if Review.objects.filter(author=request.user,
                                     title=title).exists():
                raise serializers.ValidationError(
                    'Ваш отзыв уже есть.')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментарие."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'text', 'author', 'pub_date']
        read_only = ['id']


class UserSerializer(serializers.ModelSerializer):
    """Сериализер для создания User."""

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        max_length=settings.MAX128,
        required=True
    )
    username = serializers.RegexField(
        max_length=settings.MAX128,
        required=True,
        regex=r'^[\w.@+-]+\Z',
        validators=[validate_username]
    )
