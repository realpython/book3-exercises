from django.test import TestCase
from main.models import StatusReport
from main.serializers import StatusReportSerializer
from django.test import RequestFactory
from main.json_views import StatusCollection, StatusMember
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate
from payments.models import User

class JsonViewTests(TestCase):


    @classmethod
    def setUpClass(cls):
        cls.factory = APIRequestFactory()
        cls.test_user = User(id=2222, email="test@user.com")

    def get_request(self,method='GET', authed=True):
        request_method = getattr(self.factory, method.lower())
        request = request_method("")
        if authed:
            force_authenticate(request, self.test_user)

        return request


    def test_get_collection(self):
        status = StatusReport.objects.all()
        expected_json = StatusReportSerializer(status, many=True).data

        response = StatusCollection.as_view()(self.get_request())
        self.assertEqual(expected_json,response.data)
 
    def test_get_collection_requires_logged_in_user(self):
        response = StatusCollection.as_view()(self.get_request(authed=False))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_member(self):
        stat = StatusReport(user=self.test_user, status="testing")
        stat.save()

        response =StatusMember.as_view()(
            self.get_request(method='DELETE'), pk=stat.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_memeber(self):
        status = StatusReport.objects.get(pk=1)
        expected_json = StatusReportSerializer(status).data

        response = StatusMember.as_view()(self.get_request(), pk=1)

        self.assertEqual(expected_json, response.data)
