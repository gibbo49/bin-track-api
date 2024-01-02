"""
Views for the bin details API.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import BinObject
from detail import serializers


class BinViewSet(viewsets.ModelViewSet):
    """View for manage bin detail APIs."""
    serializer_class = serializers.BinSerializer
    queryset = BinObject.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve bins for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')
