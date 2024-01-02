"""
Test for bin detail APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import BinObject

from detail.serializers import BinSerializer


BINS_URL = reverse('detail:detail-list')


def create_bin(user, **params):
    """Create and return a sample bin object."""
    defaults = {
        'bin_id': 8607,
        'bin_size': '32m',
        'bin_type': 'Open Skip',
        'bin_special': True,
        'special_bin_owner': 'Huhtamaki',
        'bin_owner_id': 80083466,
        'bin_location': 'Bin Yard - Glendenning',
        'bin_tagged_out': False,
        'bin_defects': 'Door Lock Broken',
    }
    defaults.update(params)

    detail = BinObject.objects.create(user=user, **defaults)
    return detail


class PublicBinAPITests(TestCase):
    """Test unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(BINS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateBinAPITests(TestCase):
    """Test authenticated API"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_bins(self):
        """Test retrieving a list of bins."""
        create_bin(user=self.user)
        create_bin(user=self.user)

        res = self.client.get(BINS_URL)

        details = BinObject.objects.all().order_by('-id')
        serializer = BinSerializer(details, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_bin_list_limited_to_user(self):
        """Test list of bins is limited to authenticated users."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'passsword123',
        )
        create_bin(user=other_user)
        create_bin(user=self.user)

        res = self.client.get(BINS_URL)

        details = BinObject.objects.filter(user=self.user)
        serializer = BinSerializer(details, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
