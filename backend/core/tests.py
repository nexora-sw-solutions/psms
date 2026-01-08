from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Organization
from django.utils.crypto import get_random_string


class Phase1Tests(TestCase):
    def setUp(self):
        # Create an organization
        self.org = Organization.objects.create(name="Test Org")

        # Create a FIRM_ADMIN user
        self.admin_user = User.objects.create_user(
            email="admin@test.com",
            password="AdminPass123!",
            role=User.Role.FIRM_ADMIN,
            organization=self.org
        )

        # Create a normal consultant user
        self.consultant_user = User.objects.create_user(
            email="consultant@test.com",
            password="ConsultPass123!",
            role=User.Role.CONSULTANT,
            organization=self.org
        )

        self.client = APIClient()

    def test_organization_creation(self):
        """Test Organization model"""
        org_count = Organization.objects.count()
        self.assertEqual(org_count, 1)
        self.assertEqual(self.org.name, "Test Org")

    def test_user_invitation(self):
        """Test inviting a new user via API"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("user_invite")
        data = {
            "email": "staff1@test.com",
            "role": "CONSULTANT"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check user exists
        self.assertTrue(User.objects.filter(email="staff1@test.com").exists())

    def test_invite_forbidden_for_non_admin(self):
        """CONSULTANT should not be able to invite"""
        self.client.force_authenticate(user=self.consultant_user)
        url = reverse("user_invite")
        data = {"email": "staff2@test.com", "role": "CONSULTANT"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_get(self):
        """User can view their own profile"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("user_profile", args=[self.admin_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.admin_user.email)

    def test_profile_patch(self):
        """User can update their own profile"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("user_profile", args=[self.admin_user.id])
        data = {"first_name": "John", "last_name": "Doe"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.admin_user.refresh_from_db()
        self.assertEqual(self.admin_user.first_name, "John")
        self.assertEqual(self.admin_user.last_name, "Doe")

    def test_profile_forbidden_other_user(self):
        """Users cannot access another user's profile"""
        self.client.force_authenticate(user=self.consultant_user)
        url = reverse("user_profile", args=[self.admin_user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)