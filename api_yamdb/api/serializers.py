from rest_framework import serializers
from reviews.models import Category, Genre, Title


class TitleSerializer(serializers.ModelSerializer):
    """Сериализер модели Title."""
    category = serializers.SlugRelatedField(slug_field='slug',
                                            queryset=Category.objects.all(),
                                            required=False)
    genre = serializers.SlugRelatedField(slug_field='slug',
                                         queryset=Genre.objects.all(),
                                         many=True)

    class Meta:
        model = Title
        fields = ['id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category']


class GenreSerializer(serializers.ModelSerializer):
    """Сериализер модели Genre."""
    class Meta:
        model = Genre
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализер модели Category."""
    class Meta:
        model = Category
        fields = ['name', 'slug']
        read_only_fields = ['slug']


class SignUpSerializer(serializers.Serializer):
    """Сериализер регистрации."""
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)


class TokenSerializer(serializers.Serializer):
    """Сериализер отправки токена."""
    username = serializers.CharField(max_length=30)
    confirmation_code = serializers.CharField(max_length=255)
