from payments.views import sign_in, sign_out, register, soon
from django.test import TestCase, RequestFactory
from payments.models import User
from payments.forms import SigninForm, UserForm
from django.db import IntegrityError
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
import django_ecommerce.settings as settings
import mock


class ViewTesterMixin(object):

    @classmethod
    def setupViewTester(cls, url, view_func, expected_html,
                        status_code=200,
                        session={}):
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
        html = render_to_response(
            'sign_in.html',
            {
                'form': SigninForm(),
                'user': None
            }
        )

        ViewTesterMixin.setupViewTester(
            '/sign_in',
            sign_in,
            html.content
        )


class SignOutPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        ViewTesterMixin.setupViewTester(
            '/sign_out',
            sign_out,
            "",  # a redirect will return no html
            status_code=302,
            session={"user": "dummy"},
        )

    def setUp(self):
        #sign_out clears the session, so let's reset it everytime
        self.request.session = {"user": "dummy"}


class RegisterPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        html = render_to_response(
            'register.html',
            {
                'form': UserForm(),
                'months': range(1, 12),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': range(2011, 2036),
            }
        )
        ViewTesterMixin.setupViewTester(
            '/register',
            register,
            html.content,
        )

    def setUp(self):
        request_factory = RequestFactory()
        self.request = request_factory.get(self.url)

    def test_invalid_form_returns_registration_page(self):

        with mock.patch('payments.forms.UserForm.is_valid') as user_mock:

            user_mock.return_value = False

            self.request.method = 'POST'
            self.request.POST = None
            resp = register(self.request)
            self.assertEquals(resp.content, self.expected_html)

            # make sure that we did indeed call our is_valid function
            self.assertEquals(user_mock.call_count, 1)

    @mock.patch('payments.views.Customer.create')
    @mock.patch.object(User, 'create')
    def test_registering_new_user_returns_succesfully(
        self, create_mock, stripe_mock
    ):

        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'python@rocks.com',
            'name': 'pyRock',
            'stripe_token': '...',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password',
        }

        #get the return values of the mocks, for our checks later
        new_user = create_mock.return_value
        new_cust = stripe_mock.return_value

        resp = register(self.request)

        self.assertEquals(resp.content, "")
        self.assertEquals(resp.status_code, 302)
        self.assertEquals(self.request.session['user'], new_user.pk)
        #verify the user was actually stored in the database.
        create_mock.assert_called_with(
            'pyRock', 'python@rocks.com', 'bad_password', '4242', new_cust.id
        )

    # old test
    # def test_registering_new_user_returns_succesfully(self):

    #     self.request.session = {}
    #     self.request.method = 'POST'
    #     self.request.POST = {
    #         'email': 'python@rocks.com',
    #         'name': 'pyRock',
    #         'stripe_token': '...',
    #         'last_4_digits': '4242',
    #         'password': 'bad_password',
    #         'ver_password': 'bad_password',
    #     }

    #     with mock.patch('stripe.Customer') as stripe_mock:

    #         config = {'create.return_value': mock.Mock()}
    #         stripe_mock.configure_mock(**config)

    #         resp = register(self.request)
    #         self.assertEquals(resp.content, "")
    #         self.assertEquals(resp.status_code, 302)
    #         self.assertEquals(self.request.session['user'], 1)

    #         # verify the user was actually stored in the database.
    #         # if the user is not there this will throw an error
    #         User.objects.get(email='python@rocks.com')

    def get_MockUserForm(self):
        from django import forms

        class MockUserForm(forms.Form):

            def is_valid(self):
                return True

            @property
            def cleaned_data(self):
                return {
                    'email': 'python@rocks.com',
                    'name': 'pyRock',
                    'stripe_token': '...',
                    'last_4_digits': '4242',
                    'password': 'bad_password',
                    'ver_password': 'bad_password',
                }

            def addError(self, error):
                pass

        return MockUserForm()

    @mock.patch('payments.views.UserForm', get_MockUserForm)
    @mock.patch('payments.models.User.save', side_effect=IntegrityError)
    def test_registering_user_twice_cause_error_msg(self, save_mock):

        #create the request used to test the view
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {}

        #create the expected html
        html = render_to_response(
            'register.html',
            {
                'form': self.get_MockUserForm(),
                'months': list(range(1, 12)),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': list(range(2011, 2036)),
            }
        )

        #mock out stripe so we don't hit their server
        with mock.patch('payments.views.Customer') as stripe_mock:

            config = {'create.return_value': mock.Mock()}
            stripe_mock.configure_mock(**config)

            #run the test
            resp = register(self.request)

            #verify that we did things correctly
            self.assertEqual(resp.content, html.content)
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(self.request.session, {})

            #assert there is no records in the database.
            users = User.objects.filter(email="python@rocks.com")
            self.assertEqual(len(users), 0)
