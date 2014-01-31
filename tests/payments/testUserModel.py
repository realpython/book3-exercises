from django.test import TestCase, SimpleTestCase
from payments.models import User
import mock
from django.db import IntegrityError

class UserModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = User(email = "j@j.com", name ='test user')
        cls.test_user.save()

    def test_user_to_string_print_email(self):
        self.assertEqual(str(self.test_user), "j@j.com")
       
    def test_get_by_id(self):
        self.assertEqual(User.get_by_id(1), self.test_user)

    def test_create_user_function_stores_in_database(self):
        user = User.create("test", "test@t.com","tt","1234","22")
        self.assertEqual(User.objects.get(email="test@t.com"), user)

    def test_create_user_allready_exists_throws_IntegrityError(self):
        from django.db import IntegrityError
        self.assertRaises(IntegrityError, User.create, "test user",
                          "j@j.com","jj","1234",89)



from payments.forms import SigninForm, CardForm, UserForm
import unittest
from pprint import pformat

class FormTesterMixin(): 


    def shouldHaveFormError(self, form_cls, expected_error_name, expected_error_msg,
                        data):

        from pprint import pformat
        test_form = form_cls(data=data)
        #if we get an error then the form should not be valid
        self.assertFalse(test_form.is_valid())

        self.assertEqual(test_form.errors[expected_error_name],
                           expected_error_msg,
                           msg= "Expected %s : Actual %s : using data %s" % 
                           (test_form.errors[expected_error_name], 
                           expected_error_msg, pformat(data)))

class FormTests(SimpleTestCase, FormTesterMixin):
    
    def test_signin_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': { 'email' : 'j@j.com'},
             'error': ('password' , ['This field is required.'])},
            {'data': {'password' : '1234'},
             'error' : ('email' , ['This field is required.'])}
        ]

        for invalid_data in invalid_data_list:
            self.shouldHaveFormError(SigninForm,
                                 invalid_data['error'][0],
                                 invalid_data['error'][1],
                                 invalid_data["data"])

    def test_card_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': {'last_4_digits' : '123'},
             'error' : ('last_4_digits', ['Ensure this value has at least 4 characters (it has 3).'])},
            {'data': {'last_4_digits' : '12345'},
             'error' : ('last_4_digits', ['Ensure this value has at most 4 characters (it has 5).'])}
            ]

        for invalid_data in invalid_data_list:
             self.shouldHaveFormError(CardForm,
                                  invalid_data['error'][0],
                                  invalid_data['error'][1],
                                   invalid_data["data"])


    def test_user_form_passwords_match(self):
        form = UserForm({'name' : 'jj', 'email': 'j@j.com', 'password' : '1234',
                         'ver_password' : '1234', 'last_4_digits' : '3333',
                         'stripe_token': '1'})

        self.assertTrue(form.is_valid())
        #this will throw an error if it doesn't clean correctly
        self.assertIsNotNone(form.clean())

    def test_user_form_passwords_dont_match_throws_error(self):
        form = UserForm({'name' : 'jj', 'email': 'j@j.com', 'password' : '234',
                         'ver_password' : '1234', 'last_4_digits' : '3333',
                         'stripe_token': '1'})

        self.assertFalse(form.is_valid())

        from django import forms
        self.assertRaisesMessage(forms.ValidationError, 
                                 "Passwords do not match",
                                 form.clean)


