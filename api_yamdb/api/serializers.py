from rest_framework import serializers

from reviews.models import Category, Comments, Genre, Reviews, Title


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


class ReviewsSerializer(serializers.ModelSerializer):
    """Сериализатор для отзыввов."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    score = serializers.IntegerField(max_value=10, min_value=1)

    class Meta:
        model = Reviews
        fields = ['id', 'text', 'author', 'score', 'pub_date']
        read_only = ['id']

    def validate(self, data):
        request = self.context['request']
        title = self.context['view'].kwargs.get('title_id')
        if request.method == 'POST':
            if Reviews.objects.filter(author=request.user,
                                      title=title).exists():
                raise serializers.ValidationError(
                    'Ваш отзыв уже есть.')
        return data


class CommentsSerializer(serializers.ModelSerializer):
    """Сериализатор для комментарие."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comments
        fields = ['id', 'text', 'author', 'pub_date']
        read_only = ['id']
