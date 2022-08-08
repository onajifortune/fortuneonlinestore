from rest_framework.test import APITestCase

from account.models import Customer

# Create your tests here.


class TestModel(APITestCase):

    def test_creates_user(self):
        user = Customer.objects.create_user(
            email='a@a.com', user_name='Fortune', password='abcd1234')
        self.assertIsInstance(user, Customer)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.email, 'a@a.com')

    def test_creates_superuser(self):
        user = Customer.objects.create_superuser(
            email='a@a.com', user_name='admin', password='abcd1234')
        self.assertIsInstance(user, Customer)
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertEqual(user.email, 'a@a.com')

    def test_is_superuser_raises_error_is_staff_is_false(self):
        self.assertRaises(ValueError, Customer.objects.create_superuser,
                          user_name="admin", email='a@a.com', password='abcd1234', is_staff=False)

    def test_is_superuser_raises_error_is_superuser_is_false(self):
        self.assertRaises(ValueError, Customer.objects.create_superuser,
                          user_name="admin", email='a@a.com', password='abcd1234', is_superuser=False)

    def test_no_email_raises_error(self):
        self.assertRaises(ValueError, Customer.objects.create_user,
                          user_name="admin", email='', password='abcd1234')

    def test_string_return_user_name(self):
        user = Customer.objects.create_user(
            email='a@a.com', user_name='Fortune', password='abcd1234')
        check = Customer.__str__(user)
        self.assertEqual(check, 'Fortune')
