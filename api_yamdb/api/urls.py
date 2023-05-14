from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (TitleViewSet, GenreViewSet, CategoryViewSet,
                    signup, authtoken)

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', authtoken)
]
