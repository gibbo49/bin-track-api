"""
URL mappings for thee bin app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from detail import views


router = DefaultRouter()
router.register('details', views.BinViewSet)

app_name = 'detail'

urlpatterns = [
    path('', include(router.urls)),
]
