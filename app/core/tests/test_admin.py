from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@altafQUIRK.COM", password="Quirky@123"
        )

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="testuser@quirkyaltaf.com",
            password="password@123",
            name="test user fullname",
        )

    def test_users_listed(self):
        """test that users are listed on user page"""
        url = reverse("admin:core_user_changelist")

        # below line works as a demo browser make a get request to given url
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        # /admin/core/user/1
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """test that user creation page works"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
