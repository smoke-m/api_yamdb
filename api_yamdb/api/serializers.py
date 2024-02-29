from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db.models import Avg
# from django.shortcuts import get_object_or_404

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
    # rating = serializers.IntegerField(
    #     source='reviews__score__avg', read_only=True)
    rating = serializers.SerializerMethodField(read_only=True)

    def get_rating(self, instance):
        rating = instance.reviews.aggregate(
            avg_rating=Avg('score'))['avg_rating']
        return rating

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


class GetContextTitle():
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context.get('view').kwargs.get('title_id')


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыввов."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault())
    score = serializers.IntegerField(validators=max_min_validator())
    title = serializers.HiddenField(default=GetContextTitle())

    class Meta:
        model = Review
        fields = ['id', 'text', 'author', 'score', 'pub_date', 'title']
        read_only = ['id']
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title'),
                message='Ваш отзыв уже есть.'
            )
        ]

    # оставил чобы помнить альтернативу.
    # def validate(self, data):
    #     if self.context['request'].method == 'POST':
    #         if Review.objects.filter(
    #             author=self.context['request'].user,
    #             title=get_object_or_404(
    #                 Title,
    #                 id=self.context['view'].kwargs.get('title_id'),
    #             ),
    #         ).exists():
    #             raise serializers.ValidationError('Ваш отзыв уже есть.')
    #     return data


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
        max_length=settings.EMAIL_LENGTH,
        required=True
    )
    username = serializers.RegexField(
        max_length=settings.USERNAME_LENGTH,
        required=True,
        regex=r'^[\w.@+-]+\Z',
        validators=[validate_username]
    )
