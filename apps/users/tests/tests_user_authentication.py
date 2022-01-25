from django.contrib.auth import get_user_model
from django.test import TestCase


class UsersManagersTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='kamran@user.com', username='Kamranthebest', password='verystongpass')
        self.assertEqual(user.email, 'kamran@user.com')
        self.assertEqual(user.username, 'Kamranthebest')

        self.assertTrue(user.is_active)
        self.assertFalse(user.is_verified)

        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', username='Kamran', password="foo")
        with self.assertRaises(ValueError):
            User.objects.create_user(email='kamran@mail.ru', username='', password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='kamran@user.com', username='Kamranthebest', password='verystongpass')
        self.assertEqual(admin_user.email, 'kamran@user.com')
        self.assertEqual(admin_user.username, 'Kamranthebest')

        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_verified)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='kamran@user.com', password='verystongpass', username='Kamran', is_superuser=False)

        with self.assertRaises(TypeError):
            User.objects.create_superuser(password='verystongpass', username='Kamran')

        with self.assertRaises(TypeError):
            User.objects.create_superuser(email='kamran@user.com', password='verystongpass')
