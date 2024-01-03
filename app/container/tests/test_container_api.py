"""
Test for container APIs.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Container

from container.serializers import (
    ContainerSerializer,
    ContainerDetailSerializer,
)


CONTAINER_URL = reverse('container:container-list')


def detail_url(container_id):
    """Create and return a container detail URL."""
    return reverse('container:container-detail')


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


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


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
        self.user = create_user(email='user@example.com', password='testp123')
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
        other_user = create_user(email='other@example.com', password='passw123')
        create_container(user=other_user)
        create_container(user=self.user)

        res = self.client.get(CONTAINER_URL)

        containers = Container.objects.filter(user=self.user)
        serializer = ContainerSerializer(containers, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_get_container_detail(self):
        """Test get container detail."""
        container = create_container(user=self.user)

        url = detail_url(container.id)
        res = self.client.get(url)

        serializer = ContainerDetailSerializer(container)
        self.assertEqual(res.data, serializer.data)

    def test_create_container(self):
        """Test creating a container."""
        payload = {
            'bin_id': 8607,
            'bin_size': '32m',
            'bin_type': 'Open Skip',
        }
        res = self.client.post(CONTAINER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        container = Container.objects.get(id=res.data['id'])
        for k, v in payload.items():
            self.assertEqual(getattr(container, k), v)
        self.assertEqual(container.user, self.user)

    def test_partial_update(self):
        """Test partial update of a container."""
        original_size = '32m'
        container = create_container(
            user=self.user,
            bin_id=8607,
            bin_size=original_size,
        )

        payload = {'bin_id':8000}
        url = detail_url(container.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        container.refresh_from_db()
        self.assertEqual(container.bin_id, payload['bin_id'])
        self.assertEqual(container.bin_size, original_size)
        self.assertEqual(container.user, self.user)

    def test_full_update(self):
        """Test full update of a container."""
        container = create_container(
            user=self.user,
            bin_id=1234,
            bin_size='15m',
            bin_type='Compactor',
        )

        payload = {
            'bin_id': 4321,
            'bin_size': '23m',
            'bin_type': 'Unipack'
        }
        url = detail_url(container.id)
        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        container.refresh_from_db()
        for k, v in payload.items():
            self.assertEqual(getattr(container, k), v)
        self.assertEqual(container.user, self.user)

    def test_update_user_returns_error(self):
        """Test changing the container user results in an error"""
        new_user = create_user(email='user2@example.com', password='test123')
        container = create_container(user=self.user)

        payload = {'user': new_user.id}
        url = detail_url(container.id)
        self.client.patch(url, payload)

        container.refresh_from_db()
        self.assertEqual(container.user, self.user)

    def test_delete_container(self):
        """Test deleting a container successfully."""
        container = create_container(user=self.user)

        url = detail_url(container.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Container.objects.filter(id=container.id).exists())
