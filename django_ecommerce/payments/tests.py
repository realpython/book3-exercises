from django.test import TestCase
from .models import User


class UserModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = User(email = "j@j.com", name ='test user')
        cls.test_user.save()

    def test_user_to_string_print_email(self):
        self.assertEquals(str(self.test_user), "j@j.com")
       
    def test_get_by_id(self):
        self.assertEquals(User.get_by_id(1), self.test_user)

from .forms import SigninForm, CardForm
import unittest
from pprint import pformat

class FormTesterMixin():


    def assertFormError(self, form_cls, expected_error_name, expected_error_msg,
                        data):

        from pprint import pformat
        test_form = form_cls(data=data)
        #if we get an error then the form should not be valid
        self.assertFalse(test_form.is_valid())

        self.assertEquals(test_form.errors[expected_error_name],
                           expected_error_msg,
                           msg= "Expected %s : Actual %s : using data %s" % 
                           (test_form.errors[expected_error_name], 
                           expected_error_msg, pformat(data)))

class FormTests(unittest.TestCase, FormTesterMixin):
    
    def test_signin_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': { 'email' : 'j@j.com'},
             'error': ('password' , [u'This field is required.'])},
            {'data': {'password' : '1234'},
             'error' : ('email' , [u'This field is required.'])}
        ]

        for invalid_data in invalid_data_list:
            self.assertFormError(SigninForm,
                                 invalid_data['error'][0],
                                 invalid_data['error'][1],
                                 invalid_data["data"])

    def test_card_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': {'last_4_digits' : '123'},
             'error' : ('last_4_digits', [u'Ensure this value has at least 4 characters (it has 3).'])},
            {'data': {'last_4_digits' : '12345'},
             'error' : ('last_4_digits', [u'Ensure this value has at most 4 characters (it has 5).'])}
            ]

        for invalid_data in invalid_data_list:
             self.assertFormError(CardForm,
                                  invalid_data['error'][0],
                                  invalid_data['error'][1],
                                  invalid_data["data"])
