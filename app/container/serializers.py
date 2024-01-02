"""
Serializers for container APIs.
"""
from rest_framework import serializers

from core.models import Container


class ContainerSerializer(serializers.ModelSerializer):
    """Serializer for containers."""

    class Meta:
        model = Container
        fields = ['id', 'bin_id', 'bin_size', 'bin_type']
        read_only_fields = ['id']
