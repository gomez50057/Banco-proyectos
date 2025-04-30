# formulario/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NivelacionTierraViewSet,
    ArchivoPDFViewSet,
    NivelacionTierraUserViewSet,
)

router = DefaultRouter()
router.register('formularios', NivelacionTierraViewSet)
router.register('archivos', ArchivoPDFViewSet)
router.register('nivelaciones', NivelacionTierraUserViewSet, basename='nivelaciones')

urlpatterns = [
    path('', include(router.urls)),
]
