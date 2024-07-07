from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminsiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='password123',
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='password123',
            name='zeus',
        )



    def test_create_user_page(self):
        url = reverse('admin:core_user_add')
        res = self.client.post(url,{
            'password':'kelvin.123',
            'email':'kelvin.123',
            'phone':'09067536857',
            'firstName':'kelvin',
            'lastName':'joshua'})
        self.assertEqual(res.status_code,201)