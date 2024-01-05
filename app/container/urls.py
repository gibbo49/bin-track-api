"""
URL mappings for the container app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from container import views


router = DefaultRouter()
router.register('containers', views.ContainerViewSet)
router.register('tags', views.TagViewSet)

app_name = 'container'

urlpatterns = [
    path('', include(router.urls)),
]
