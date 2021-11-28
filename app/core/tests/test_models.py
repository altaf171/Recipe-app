from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        'test creating new user with email and password'
        email = 'testpy98@outlook.com'
        password = 'Kartoon#12'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalize(self):
        '''test if the  new user's email is normalize'''
        email = 'test@ALTAFQUIRK.COM'
        user = get_user_model().objects.create_user(email, 'Kartoon#12')

        self.assertEqual(user.email, email.lower())

    def test_user_invalid_email(self):
        '''test that if email provided is valid or not
        without email raise error
        '''
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Kartoon#12')

    def test_create_new_super_user(self):
        '''test creating new super user'''
        user = get_user_model().objects.create_superuser(
            'test@ALTAFQUIRK.COM', 'Kartoon#12')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
