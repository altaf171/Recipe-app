from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient

from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    """tests users api (public)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """testing that creating user with valid payload is successful"""
        payload = {
            "name": "Tinda Aaloo",
            "email": "tinda@quirky.com",
            "password": "bhindiisgood",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_user_exist(self):
        """test that if user already exist"""
        payload = {"email": "tinda@quirky.com", "password": "bhindiisgood"}

        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """test that password must be more than 5 charector long"""
        payload = {"email": "tinda@quirky.com", "password": "bin"}
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(email=payload["email"]).exists()

        self.assertFalse(user_exist)

    def test_create_token_for_user(self):
        """test that token for user is created"""
        payload = {"email": "tinda@quirky.com", "password": "bhindiisgood"}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn("token", res.data)

    def test_create_token_invalid_credentials(self):
        """test that token is not created if invalid credentials are given"""
        payload = {"email": "tinda@quirky.com", "password": "bhindiisgood"}
        create_user(**payload)
        payload_wrong_pass = {"email": "tinda@quirky.com", "password": "wrongpass"}
        res = self.client.post(TOKEN_URL, payload_wrong_pass)
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {"email": "tinda@quirky.com", "password": "bhindiisgood"}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {"email": "one", "password": ""})
        self.assertNotIn("token", res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
