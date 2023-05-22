from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import IntegrityError
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (filters, mixins, permissions, serializers, status,
                            viewsets)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import Category, Genre, Review, Title, User
from .filters import TitleFilter
from .permissions import AuthorOrReadOnly, IsAdmin
from .serializers import (CategorySerializer, CommentsSerializer,
                          GenreSerializer, ReviewsSerializer, SignUpSerializer,
                          TitleSerializerRead, TitleSerializerWrite,
                          TokenSerializer, UserSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """View модели Title."""
    queryset = Title.objects.all().annotate(
        Avg('reviews__score')).order_by('-id')
    permission_classes = [IsAdmin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializerRead
        return TitleSerializerWrite


class GenreCategoryMixinsSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Сет миксинов для: Genre, Category."""
    pass


class GenreViewSet(GenreCategoryMixinsSet):
    """View модели Genre."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class CategoryViewSet(GenreCategoryMixinsSet):
    """View модели Category."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdmin]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def signup(request):
    """Отправляет сообщение с кодом при регистрации."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, created = User.objects.get_or_create(
            username=request.data.get('username'),
            email=request.data.get('email'))
    except IntegrityError:
        raise serializers.ValidationError(
            'Пользователь с таким email уже существует.')
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация.',
        message=f'Код подтверждения для токена: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def authtoken(request):
    """Авторизация пользователя."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(
        user, serializer.validated_data["confirmation_code"]
    ):
        token = AccessToken.for_user(user)
        return Response({'token': str(token)}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewsViewSet(viewsets.ModelViewSet):
    """View отзывов."""
    serializer_class = ReviewsSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())

    def get_queryset(self):
        return self.get_title().reviews.all()


class CommentsViewSet(viewsets.ModelViewSet):
    """View комментариев."""
    serializer_class = CommentsSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs['review_id'],
            title_id=self.kwargs['title_id'],
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())

    def get_queryset(self):
        return self.get_review().comments.all()


class UserViewSet(viewsets.ModelViewSet):
    """View UseroB."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin, permissions.IsAuthenticated)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        methods=('get', 'patch'),
        detail=False,
        url_path='me',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def me(self, request, pk=None):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserSerializer(request.user,
                                        data=request.data,
                                        partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)
