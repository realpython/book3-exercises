from django.test import TestCase
from django.core.urlresolvers import resolve
from .views import index

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

    def test_returns_exact_html(self):
        index = self.client.get("/")
        from django.shortcuts import render_to_response
        self.assertEquals(index, render_to_response("index.html"))

        #ok we know it's returning something
        #ass self.assertTrue('blah' in index.context)
        #.. but that's brital and it's a constant so add
        #rendepr_to_response
        #so then do with still need our resolve test?  yes look at error
        #message
        #then test the interaction with the user session
