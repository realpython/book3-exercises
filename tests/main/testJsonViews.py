from django.test import TestCase
from main.models import StatusReport
from main.serializers import StatusReportSerializer
from main.json_views import StatusCollection
from django.test import RequestFactory
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse

class dummyRequest(object):

    class dummyUser(object):

       is_authed = True
        
       def is_authenticated(self):
            return self.is_authed

    def __init__(self, method,authed=True):
        self.method = method
        self.encoding = 'utf8'
        self.user = self.dummyUser()
        self.user.is_authed = authed
        self.successful_authenticator = True
        self.QUERY_PARAMS = {}
        self.META = {}


class JsonViewTests(TestCase):

    def test_get_collection(self):
        status = StatusReport.objects.all()
        expected_json = StatusReportSerializer(status, many=True).data
        response = StatusCollection.as_view()(dummyRequest("GET"))

        self.assertEqual(expected_json,response.data)
 
    def test_get_collection_requires_logged_in_user(self):
        anon_request = dummyRequest("GET", authed=False)
        response = StatusCollection.as_view()(anon_request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)




