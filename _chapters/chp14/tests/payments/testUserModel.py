from django.test import TestCase
from payments.models import User
from django.db import IntegrityError

class UserModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super(UserModelTest, cls).setUpClass()
        cls.test_user = User(email="j@j.com", name='test user',
                             password="pass", last_4_digits="1234")
        cls.test_user.save()

    def test_user_to_string_print_email(self):
        self.assertEqual(str(self.test_user), "j@j.com")

    def test_get_by_id(self):
        self.assertEqual(User.get_by_id(self.test_user.id), self.test_user)

    def test_create_user_function_stores_in_database(self):
        self.assertEqual(User.objects.get(email="j@j.com"), self.test_user)

    def test_create_user_allready_exists_throws_IntegrityError(self):
        from django.db import IntegrityError
        self.assertRaises(
            IntegrityError,
            User.create,
            "test user",
            "j@j.com",
            "jj",
            "1234",
            89
        )
