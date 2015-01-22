from payments.views import sign_in, sign_out, register, edit
from django.test import TestCase
from payments.models import User, UnpaidUsers
from django.db import IntegrityError
import mock
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from payments.forms import SigninForm, CardForm, UserForm
import socket
import unittest
from django.db import transaction
from django.db import DatabaseError

class ViewTesterMixin(object):

    @classmethod
    def setupViewTester(cls, url, view_func, expected_html,
                              status_code = 200,
                              session={}):
        from django.test import RequestFactory
        request_factory = RequestFactory()
        cls.request = request_factory.get(url)
        cls.request.session = session
        cls.status_code = status_code
        cls.url = url
        cls.view_func = staticmethod(view_func)
        cls.expected_html = expected_html
    
    def test_resolves_to_correct_view(self):
        test_view = resolve(self.url)
        self.assertEqual(test_view.func, self.view_func)

    def test_returns_appropriate_respose_code(self):
        resp = self.view_func(self.request)
        self.assertEqual(resp.status_code, self.status_code)

    def test_returns_correct_html(self):
        resp = self.view_func(self.request)
        self.assertEqual(resp.content, self.expected_html)

class SignInPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        html = render_to_response('payments/sign_in.html',
        {
          'form': SigninForm(),
          'user': None
        })

        ViewTesterMixin.setupViewTester('/sign_in',
                                              sign_in,
                                              html.content)
    
class SignOutPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        ViewTesterMixin.setupViewTester('/sign_out',
                                        sign_out,
                                        b"", #a redirect will return no html
                                        status_code=302,
                                        session={"user":"dummy"},
                                       )
    def setUp(self):
        #sign_out clears the session, so let's reset it everytime
        self.request.session = {"user":"dummy"}

import django_ecommerce.settings as settings
from payments.views import soon
class RegisterPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        html = render_to_response('payments/register.html',
        {
          'form': UserForm(),
          'months': list(range(1, 12)),
          'publishable': settings.STRIPE_PUBLISHABLE,
          'soon': soon(),
          'user': None,
          'years': list(range(2011, 2036)),
        })
        ViewTesterMixin.setupViewTester('/register',
                                        register,
                                        html.content,
                                       )
    def setUp(self):
        from django.test import RequestFactory
        request_factory = RequestFactory()
        self.request = request_factory.get(self.url)

    
    def get_MockUserForm(self):
        from django import forms
        class MockUserForm(forms.Form):

            def is_valid(self):
                return True

            @property
            def cleaned_data(self):
                return {'email' : 'python@rocks.com',
                             'name' : 'pyRock',
                             'stripe_token' : '...',
                             'last_4_digits' : '4242',
                             'password' : 'bad_password',
                             'ver_password' : 'bad_password',
                            }
            def addError(self, erro):
                pass

        return MockUserForm()

    @mock.patch('payments.models.UnpaidUsers.save', side_effect =
                IntegrityError)
    def test_registering_user_when_strip_is_down_all_or_nothing(self, save_mock):
        
        #create the request used to test the view
        self.request.session = {}
        self.request.method='POST'
        self.request.POST = {'email' : 'python@rocks.com',
                             'name' : 'pyRock',
                             'stripe_token' : '...',
                             'last_4_digits' : '4242',
                             'password' : 'bad_password',
                             'ver_password' : 'bad_password',
                            }        


        #mock out stripe so and ask it to throw a connection error
        with mock.patch('stripe.Customer.create', side_effect =
                        socket.error("can't connect to stripe")) as stripe_mock:

            #run the test
            resp = register(self.request)

        
            #assert there is a record in the database without stripe id.
            users = User.objects.filter(email="python@rocks.com")
            self.assertEqual(len(users), 0)

            #check the associated table got updated.
            unpaid = UnpaidUsers.objects.filter(email="python@rocks.com")
            self.assertEqual(len(unpaid), 0)

    
class EditPageTests(TestCase, ViewTesterMixin):

    #edit page test
    @classmethod
    def setUpClass(cls):
        ViewTesterMixin.setupViewTester('/edit',
                                        edit,
                                        b'', #a redirect will return no html
                                        status_code=302,
                                       )




