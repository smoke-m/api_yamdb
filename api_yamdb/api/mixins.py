from rest_framework import mixins, viewsets


class GenreCategoryMixinsSet(
    mixins.ListModelMixin, mixins.CreateModelMixin,
    mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """Сет миксинов для: Genre, Category."""
    pass
