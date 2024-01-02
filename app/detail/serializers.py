"""
Serializers for bin APIs.
"""
from rest_framework import serializers

from core.models import BinObject


class BinSerializer(serializers.ModelSerializer):
    """Serializer for bins."""

    class Meta:
        model = BinObject
        fields = ['id',
                  'bin_id',
                  'bin_size',
                  'bin_type',
                  'bin_special',
                  'special_bin_owner',
                  'bin_owner_id',
                  'bin_location',
                  'bin_tagged_out',
                  'bin_defects',]
        read_only_fields = ['id']
