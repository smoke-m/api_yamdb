from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title, User


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
        fields = ['name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализер модели Category."""
    class Meta:
        model = Category
        fields = ['name', 'slug']


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализер регистрации."""
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    """Сериализер отправки токена."""
    username = serializers.CharField(max_length=30)
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
    username = serializers.CharField(required=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User
