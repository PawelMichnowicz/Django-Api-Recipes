from urllib import response
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:create')
User = get_user_model()

def create_user(**params):
    return User.objects.create(**params)


class PublicUserApiTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_user_register_success(self):

        payload = {'email':'hejo1@gmail.com','password':'skuter123','name' : 'testname'}

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn(payload['password'], res.data)

    def test_user_email_exists(self):

        payload = {'email':'test@mail.com','password':'skuter123','name' : 'testname'}

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short(self):

        payload = {'email':'test@mail.com','password':'123','name' : 'testname'}

        res = self.client.post(CREATE_USER_URL, data=payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        is_exist = User.objects.filter(email=payload['email']).exists()
        self.assertFalse(is_exist)

