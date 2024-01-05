"""
Serializers for container APIs.
"""
from rest_framework import serializers

from core.models import (
    Container,
    Tag,
)


class ContainerSerializer(serializers.ModelSerializer):
    """Serializer for containers."""

    class Meta:
        model = Container
        fields = ['id', 'bin_id', 'bin_size', 'bin_type']
        read_only_fields = ['id']


class ContainerDetailSerializer(ContainerSerializer):
    """Serializer for container detail view."""

    class Meta(ContainerSerializer.Meta):
        fields = ContainerSerializer.Meta.fields + ['description']

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
