from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.validators import UnicodeUsernameValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


# class CategoryField(serializers.SlugRelatedField):
#     def to_representation(self, value):
#         serializer = CategorySerializer(value)
#         return serializer.data


# class GenreField(serializers.SlugRelatedField):
#     def to_representation(self, value):
#         serializer = GenreSerializer(value)
#         return serializer.data


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

    class Meta:
        fields = ['id', 'name', 'year', 'description', 'genre', 'category']
        model = Title

    def validate_year(self, value):
        if value >= timezone.now().year:
            raise serializers.ValidationError('Год указан не верно.')
        return value


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализер регистрации."""
    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    """Сериализер отправки токена."""
    username = serializers.CharField(max_length=30,
                                     validators=[UnicodeUsernameValidator, ])
    confirmation_code = serializers.CharField(max_length=255)


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыввов."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    score = serializers.IntegerField(max_value=10, min_value=1)

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


class ProfileSerializer(UserSerializer):
    """Серилизер для users/me"""
    role = serializers.CharField(read_only=True)
