from django.test import TestCase
from django.core.urlresolvers import resolve
from main.views import index
from main.models import MarketingItem
from payments.models import User
from django.shortcuts import render_to_response
from django.test import RequestFactory
import mock
from main.migrations.data_load_marketing_items_0003 import init_marketing_data


class MainPageTests(TestCase):

    ###############
    #### Setup ####
    ###############

    @classmethod
    def setUpClass(cls):
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}
        #[MarketingItem(**m.__dict__).save() for m in market_items]

    ##########################
    ##### Testing routes #####
    ##########################

    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    def test_returns_appropriate_html_response_code(self):
        resp = index(self.request)
        self.assertEquals(resp.status_code, 200)

    #####################################
    #### Testing templates and views ####
    #####################################

    def test_returns_exact_html(self):
        data = [MarketingItem(**d) for d in init_marketing_data]
        resp = index(self.request)
        self.assertEqual(
            resp.content,
            render_to_response(
                "main/index.html",
                {"marketing_items": data}
            ).content
        )

    def test_index_handles_logged_in_user(self):
        #create a session that appears to have a logged in user
        self.request.session = {"user": "1"}

        #setup dummy user
        #we need to save user so user -> badges relationship is created
        u = User(email="test@user.com")
        u.save()

        with mock.patch('main.views.User') as user_mock:

            #tell the mock what to do when called
            config = {'get_by_id.return_value': u}
            user_mock.configure_mock(**config)

            #run the test
            resp = index(self.request)

            #ensure we return the state of the session back to normal
            self.request.session = {}
            u.delete()

            #we are now sending a lot of state for logged in users, rather than
            #recreating that all here, let's just check for some text
            #that should only be present when we are logged in.
            self.assertContains(resp, "Report back to base")
