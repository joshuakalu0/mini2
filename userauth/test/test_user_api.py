from django.test  import  TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_USER = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        payload = {
            'name':'example',
            'email':'test@example.com',
            'password':'password123',
        }
        res = self.client.post(CREATE_USER_USER,payload)

        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email = payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_with_email_exist_error(self):
        payload = {
            'name':'example',
            'email':'test@example.com',
            'password':'password123',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_USER,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_morethan_four_charater(self):
        payload = {
            'name':'example',
            'email':'test@example.com',
            'password':'ps',
        }
        res = self.client.post(CREATE_USER_USER,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user)

    def test_create_token_for_user(self):
        model_data = {
            'name':'example',
            'email':'test@example.com',
            'password':'password123',
        }
        create_user(**model_data)
        payload = {
            'email':'test@example.com',
            'password':'password123',
        }
        res = self.client.post(TOKEN_URL,payload)

        self.assertIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_token_with_bad_details(self):
        model_data = {
            'email':'test@example.com',
            'password':'password123',
        }
        create_user(**model_data)
        payload = {
            'email':'test@example.com',
            'password':'password',
        }
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_create_token_with_black_password(self):
        payload = {
            'email':'test@example.com',
            'password':'',
        }
        res = self.client.post(TOKEN_URL,payload)

        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_retrive_user_unauthorized(self):
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code,status.HTTP_401_UNAUTHORIZED)



class PrivateUserApiTes(TestCase):
    def setUp(self) -> None:
        self.user = create_user(
            name='example',
            email='test@example.com',
            password='password123',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrive_profile_success(self):
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertIn('email',res.data)
        self.assertEqual(res.data,{
            'email':self.user.email,
            'name':self.user.name
        })
    def test_post_not_allowed(self):
        res = self.client.post(ME_URL,{})
        self.assertEqual(res.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload={
            'name':'kelvin',
            'password':'newpassword123'
        }
        res = self.client.patch(ME_URL,payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name,payload['name'])
        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertTrue(self.user.check_password(payload['password']))

    def test_delete_user_profile(self):
        res = self.client.delete(ME_URL)



