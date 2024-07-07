'''
model test
'''
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    def test_create_user_with_email_and_password(self):
        email = 'john@example.com'
        password='password123'
        user = get_user_model().objects.create_user(email=email,password=password)

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_email_normailize(self):
        sample_email=[
            ['test1@EXAMPLE.com','test1@example.com'],
            ['Test2@example.com','Test2@example.com'],
            ['TEST3@EXAMPLE.COM','TEST3@example.com'],
            ['test4@example.COM','test4@example.com'],
        ]

        for email,sample in sample_email:
            user = get_user_model().objects.create_user(email=email,password='password123')
            self.assertEqual(sample,user.email)

    def test_email_not_none(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('','passs123')


