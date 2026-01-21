from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthenticationTests(TestCase):
    def test_register_success(self):
        """Test successful user registration"""
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "password1": "testpass123",
                "password2": "testpass123",
            },
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_invalid_form(self):
        """Test registration with invalid form data"""
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser",
                "password1": "testpass123",
                "password2": "differentpass",  # Passwords don't match
            },
        )
        self.assertEqual(response.status_code, 200)  # Should render form again
        self.assertFalse(User.objects.filter(username="testuser").exists())

    def test_login_success(self):
        """Test successful login"""
        User.objects.create_user(username="testuser", password="testpass123")
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, 302)  # Should redirect to cars_list
        # Check if user is authenticated in the session
        self.assertTrue("_auth_user_id" in self.client.session)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        response = self.client.post(
            reverse("login"), {"username": "nonexistent", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)  # Should render form again
        self.assertFalse("_auth_user_id" in self.client.session)

    def test_logout(self):
        """Test logout functionality"""
        User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")
        self.assertTrue("_auth_user_id" in self.client.session)

        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)  # Should redirect to cars_list
        self.assertFalse("_auth_user_id" in self.client.session)
