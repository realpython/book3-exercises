from payments.views import sign_in, sign_out, register, edit
from django.test import TestCase
from payments.models import User
from django.db import IntegrityError
import mock
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from payments.forms import SigninForm, CardForm, UserForm
import socket
import unittest

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
        self.assertEquals(test_view.func, self.view_func)

    def test_returns_appropriate_respose_code(self):
        resp = self.view_func(self.request)
        self.assertEquals(resp.status_code, self.status_code)

    def test_returns_correct_html(self):
        resp = self.view_func(self.request)
        self.assertEquals(resp.content, self.expected_html)

class SignInPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        html = render_to_response('sign_in.html',
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
                                        "", #a redirect will return no html
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
        html = render_to_response('register.html',
        {
          'form': UserForm(),
          'months': range(1, 12),
          'publishable': settings.STRIPE_PUBLISHABLE,
          'soon': soon(),
          'user': None,
          'years': range(2011, 2036),
        })
        ViewTesterMixin.setupViewTester('/register',
                                        register,
                                        html.content,
                                       )
    def setUp(self):
        from django.test import RequestFactory
        request_factory = RequestFactory()
        self.request = request_factory.get(self.url)


    @unittest.skip("testing")
    def test_invalid_form_returns_registration_page(self):

        with mock.patch('payments.forms.UserForm.is_valid') as user_mock:
    
            user_mock.return_value = False

            self.request.method = 'POST'
            self.request.POST = None
            resp = register(self.request)
            self.assertEquals(resp.content, self.expected_html)

            #make sure that we did indeed call our is_valid function
            self.assertEquals(user_mock.call_count, 1)

    
    def get_mock_cust():
        class mock_cust():

            @property
            def id(self):
                return 1234

        return mock_cust()
    
    @mock.patch('payments.views.Customer.create', return_value =
                get_mock_cust())
    #@mock.patch.object(User,'create')
    def test_registering_new_user_returns_succesfully(self, stripe_mock):

        self.request.session = {}
        self.request.method='POST'
        self.request.POST = {'email' : 'python@rocks.com',
                             'name' : 'pyRock',
                             'stripe_token' : '...',
                             'last_4_digits' : '4242',
                             'password' : 'bad_password',
                             'ver_password' : 'bad_password',
                            }

        resp = register(self.request)

        self.assertEquals(resp.content, "")
        self.assertEquals(resp.status_code, 302)

        users = User.objects.filter(email="python@rocks.com")
        self.assertEquals(len(users), 1)
        self.assertEquals(users[0].stripe_id, '1234')


        #self.assertEquals(self.request.session['user'], new_user.pk)
        #verify the user was actually stored in the database.
        #create_mock.assert_called_with('pyRock','python@rocks.com','bad_password','4242')

    
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

    @unittest.skip("testing")
    @mock.patch('payments.views.UserForm', get_MockUserForm)
    @mock.patch('payments.models.User.save', side_effect=IntegrityError)
    def test_registering_user_twice_cause_error_msg(self, save_mock):
        
        #create the request used to test the view
        self.request.session = {}
        self.request.method='POST'
        self.request.POST = {}        

        #create the expected html
        html = render_to_response('register.html',
        {
          'form': self.get_MockUserForm(),
          'months': range(1, 12),
          'publishable': settings.STRIPE_PUBLISHABLE,
          'soon': soon(),
          'user': None,
          'years': range(2011, 2036),
        })
        


        #mock out stripe so we don't hit their server
        with mock.patch('payments.views.Customer.create') as stripe_mock:

            stripe_mock.return_value = mock.Mock()

            #run the test
            resp = register(self.request)

        
            #verify that we did things correctly
            self.assertEquals(resp.content, html.content)
            self.assertEquals(resp.status_code, 200)
            self.assertEquals(self.request.session, {})

            #assert there is no records in the database.
            users = User.objects.filter(email="python@rocks.com")
            self.assertEquals(len(users), 0)

    
    #@mock.patch('payments.views.UserForm', get_MockUserForm)
    #@mock.patch('payments.models.User.save', side_effect=IntegrityError)
    def test_registering_user_when_strip_is_down(self):
        
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
            self.assertEquals(len(users), 1)
            self.assertEquals(users[0].stripe_id, '')




class EditPageTests(TestCase, ViewTesterMixin):

    #edit page test
    @classmethod
    def setUpClass(cls):
        ViewTesterMixin.setupViewTester('/edit',
                                        edit,
                                        '', #a redirect will return no html
                                        status_code=302,
                                       )




