from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Reviews, Title
from .filters import TitleFilter
# from .permissions import IsAdminUserOrReadOnly
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewsSerializer, TitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """View модели Title."""
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class GenreViewSet(viewsets.ModelViewSet):
    """View модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(viewsets.ModelViewSet):
    """View модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewsViewSet(viewsets.ModelViewSet):
    """View отзывов."""
    serializer_class = ReviewsSerializer

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentsViewSet(viewsets.ModelViewSet):
    """View комментариев."""
    serializer_class = CommentsSerializer

    def get_review(self):
        return get_object_or_404(
            Reviews,
            id=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id'),
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()
