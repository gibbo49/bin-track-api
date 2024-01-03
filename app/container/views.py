"""
Views for the container API.
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Container
from container import serializers


class ContainerViewSet(viewsets.ModelViewSet):
    """View for manage container APIs."""
    serializer_class = serializers.ContainerDetailSerializer
    queryset = Container.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Retrieve bins for the authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.ContainerSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new container."""
        serializer.save(user=self.request.user)
