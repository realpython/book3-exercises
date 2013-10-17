from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import index
import unittest
from django.shortcuts import render_to_response

class MainPageTests(TestCase):

    @classmethod
    def setUpClass(cls):
        from django.test import RequestFactory
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}
        

    def test_root_resolves_to_main_view(self ):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    def test_returns_appropriate_html_respos_code(self):
        resp = index(self.request)
        self.assertEquals(resp.status_code,200)

    def test_returns_exact_html(self):
        resp = index(self.request)
        self.assertEquals(resp.content,
                          render_to_response("index.html").content)

    def  test_index_handles_logged_in_user(self):
        #create a session that appears to have a logged in user
        self.request.session = {"user" : "1"}
        
        import mock
        with mock.patch('main.views.User') as user_mock:
            
            #tell the mock what to do when called
            config = {'get_by_id.return_value':mock.Mock()}
            user_mock.configure_mock(**config)

            #run the test
            resp = index(self.request)

            #ensure we return the state of the session back to normal 
            self.request.session = {}
           
            expected_html = render_to_response('user.html',{'user': user_mock.get_by_id(1)})
            self.assertEquals(resp.content, expected_html.content)

