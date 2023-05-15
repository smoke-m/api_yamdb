from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import filters, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.tokens import AccessToken


from reviews.models import Category, Genre, Title, User
from .filters import TitleFilter
# from .permissions import IsAdminUserOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          SignUpSerializer, TokenSerializer)

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


@api_view(["POST"])
def signup(request):
    """Отправляет сообщение с кодом при регистрации."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid()
    serializer.save
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистация.',
        message=f'Код подтверждения для токена:{confirmation_code}',
        from_email=None,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def authtoken(request):
    """Авторизация пользователя."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid
    user = get_object_or_404(
        User,
        usernaem=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user, serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
