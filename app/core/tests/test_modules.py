'''
Tests for models
'''
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(get_user_model().objects.filter(email=email).exists())

    def test_new_user_email_normalized(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email='', password='123')

    def test_new_superuser(self):
        email = 'admin@wp.pl'
        password = '123'
        admin = get_user_model().objects.create_superuser(email, password)

        self.assertEqual(admin.email, email)
        self.assertTrue(admin.check_password(password))
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)