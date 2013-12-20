from django.test import SimpleTestCase
from payments.forms import SigninForm, CardForm, UserForm

class FormTesterMixin(): 


    def shouldHaveFormError(self, form_cls, expected_error_name, expected_error_msg,
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

class FormTests(SimpleTestCase, FormTesterMixin):
    
    def test_signin_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': { 'email' : 'j@j.com'},
             'error': ('password' , [u'This field is required.'])},
            {'data': {'password' : '1234'},
             'error' : ('email' , [u'This field is required.'])}
        ]

        for invalid_data in invalid_data_list:
            self.shouldHaveFormError(SigninForm,
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


