"""
Test for container APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework import APIClient

from core.models import Container

from container.serializers import ContainerSerializer


CONTAINER_URL = reverse('container:container-list')


def create_container(user, **params):
    """Create and return a sample container."""
    defaults = {
        'bin_id': 8607,
        'bin_size': '32m',
        'bin_type': 'Open Skip',
    }
    defaults.update(params)

    container = Container.objects.create(user=user, **defaults)
    return container


class PublicContainerApiTests(TestCase):
    """Test unauthenticated API requests."""
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(CONTAINER_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateContainerApiTests(TestCase):
    """Test authenticated API."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'user@example.com',
            'testpass123',
        )
        self.client.force_authenticate(self.user)

    def test_retrieving_containers(self):
        """Test retrieving a list of containers."""
        create_container(user=self.user)
        create_container(user=self.user)

        res = self.client.get(CONTAINER_URL)

        containers = Container.objects.all().order_by('-id')
        serializer = ContainerSerializer(containers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_container_list_limited_to_user(self):
        """Test list of bins is limited to authenticated users."""
        other_user = get_user_model().objects.create_user(
            'other@example.com',
            'password123',
        )
        create_container(user=other_user)
        create_container(user=self.user)

        res = self.client.get(CONTAINER_URL)

        containers = Container.objects.filter(user=self.user)
        serializer = ContainerSerializer(containers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
