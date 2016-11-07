from django.test import TestCase
from django.core.urlresolvers import resolve
from main.views import index
from django.shortcuts import render
from payments.models import User
from django.test import RequestFactory
import mock
from main.views import index, market_items


class MainPageTests(TestCase):
    fixtures = ['initial_data.json', ]

    ###############
    #### Setup ####
    ###############

    @classmethod
    def setUpClass(cls):
        super(MainPageTests, cls).setUpClass()
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}

    ##########################
    ##### Testing routes #####
    ##########################

    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    def test_returns_appropriate_html_response_code(self):
        resp = index(self.request)
        self.assertEqual(resp.status_code, 200)

    #####################################
    #### Testing templates and views ####
    #####################################

    def test_returns_exact_html(self):
        resp = index(self.request)
        self.assertEqual(
            resp.content,
            render(
                self.request,
                "main/index.html",
                {"marketing_items": market_items}
            ).content
        )

    def test_index_handles_logged_in_user(self):
        # Create a session that appears to have a logged in user
        self.request.session = {"user": "1"}

        with mock.patch('main.views.User') as user_mock:

            # Tell the mock what to do when called
            usr = mock.Mock()
            usr.email = "test@test.com"
            config = {'get_by_id.return_value': usr}
            user_mock.configure_mock(**config)

            # Run the test
            resp = index(self.request)

            expected_html = render(
                self.request,
                'main/user.html', {'user': user_mock.get_by_id(1)}
            )

            # Ensure we return the state of the session back to normal
            self.request.session = {}

            self.assertEqual(resp.content, expected_html.content)
