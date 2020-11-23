from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagerTest(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='bar@user.com', password='foo')

        self.assertEqual(user.email, 'bar@user.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_user_without_email(self):
        User = get_user_model()

        with self.assertRaises(ValueError):
            User.objects.create_user(email='')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('super@user.com', 'foo')

        self.assertEqual(admin_user.email, 'super@user.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class UserTest(TestCase):
    def test_str(self):
        User = get_user_model()
        user = User.objects.create_user(email='bar@foo.com', password='foo')

        self.assertEqual(user.email, str(user))
