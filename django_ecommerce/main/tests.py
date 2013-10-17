from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import index
import unittest
from django.shortcuts import render_to_response

class MainPageTests(TestCase):


    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    def test_returns_appropriate_html_respos_code(self):
        index = self.client.get('/')
        self.assertEquals(index.status_code,200)

    def test_uses_index_html_template(self):
        index = self.client.get('/')
        self.assertTemplateUsed(index, "index.html")

    def test_uses_index_html_template_2(self):
        #create a dummy request
        from django.test import RequestFactory
        request_factory = RequestFactory()
        request = request_factory.get('/')
        request.session = {} #make sure it has a session associated

        #call the view function
        resp = index(request)

        #check the response
        self.assertContains(resp, "<title>Your MVP</title>")

    def test_returns_exact_html(self):
        index = self.client.get("/")
        self.assertEquals(index.content,
                          render_to_response("index.html").content)

    def test_index_handles_logged_in_user(self):
        #create the user needed for user lookup from index page
        from payments.models import User
        user = User(
                name = 'jj',
                email = 'j@j.com',
            )
        user.save()
        
        #create a Mock request object, so we can manipulate the session
        from django.test import RequestFactory
        request_factory = RequestFactory()
        request = request_factory.get('/')
        #create a session that appears to have a logged in user
        request.session = {"user" : "1"}

        #request the index page
        resp = index(request)

        #verify it returns the page for the logged in user
        #self.assertTemplateUsed(resp, 'user.html')
        expectedHtml = render_to_response('user.html', {'user':user}).content
        self.assertEquals(resp.content,expectedHtml)
