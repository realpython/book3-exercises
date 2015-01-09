from django.test import TestCase
from payments.models import User
from django.db import IntegrityError
import datetime


class UserModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = User.create(email="j@j.com", name='test user',
                                    password="pass", last_4_digits="1234")

    @classmethod
    def tearDownClass(cls):
        cls.test_user.delete()

    def test_user_to_string_print_email(self):
        self.assertEquals(str(self.test_user), "j@j.com")

    def test_get_by_id(self):
        self.assertEqual(User.get_by_id(self.test_user.id), self.test_user)

    def test_create_user_function_stores_in_database(self):
        self.assertEquals(User.objects.get(email="j@j.com"), self.test_user)

    def test_create_user_allready_exists_throws_IntegrityError(self):
        self.assertRaises(
            IntegrityError,
            User.create,
            "test user",
            "j@j.com",
            "jj",
            "1234",
            89
        )
