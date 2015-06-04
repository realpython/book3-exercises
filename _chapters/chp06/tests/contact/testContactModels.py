from django.test import TestCase, SimpleTestCase
from contact.forms import ContactView
from contact.models import ContactForm
from datetime import datetime, timedelta


class UserModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ContactForm(email="test@dummy.com", name="test").save()
        ContactForm(email="j@j.com", name="jj").save()
        cls.firstUser = ContactForm(
            email="first@first.com",
            name="first",
            timestamp=datetime.today() + timedelta(days=2)
        )
        cls.firstUser.save()
        #cls.test_user=User(email="j@j.com", name ='test user')
        #cls.test_user.save()

    def test_contactform_str_returns_email(self):
        self.assertEqual("first@first.com", str(self.firstUser))

    def test_ordering(self):
        contacts = ContactForm.objects.all()
        self.assertEqual(self.firstUser, contacts[0])


class ContactViewTests(SimpleTestCase):

    def test_displayed_fields(self):
        expected_fields = ['name', 'email', 'topic', 'message']
        self.assertEqual(ContactView.Meta.fields, expected_fields)
