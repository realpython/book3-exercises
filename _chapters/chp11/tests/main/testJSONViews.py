from django.test import TestCase
from main.json_views import StatusCollection, StatusMember
from main.models import StatusReport
from main.serializers import StatusReportSerializer
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework import status
from payments.models import User


class JsonViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.factory = APIRequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User(id=2222, email="test@user.com")
        cls.test_user.save()


    def get_request(self, method='GET', authed=True):
        request_method = getattr(self.factory, method.lower())
        request = request_method("")
        if authed:
            force_authenticate(request, self.test_user)

        return request

    def test_get_collection(self):
        status = StatusReport.objects.all()
        expected_json = StatusReportSerializer(status, many=True).data

        response = StatusCollection.as_view()(self.get_request())
        self.assertEqual(expected_json, response.data)

    def test_get_collection_requires_logged_in_user(self):

        anon_request = self.get_request(method='GET', authed=False)
        response = StatusCollection.as_view()(anon_request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_member(self):
        stat = StatusReport(user=self.test_user, status="testing")
        stat.save()

        status = StatusReport.objects.get(pk=stat.id)
        expected_json = StatusReportSerializer(status).data

        response = StatusMember.as_view()(self.get_request(), pk=stat.id)

        self.assertEqual(expected_json, response.data)

        stat.delete()

    def test_delete_member(self):
        stat = StatusReport(user=self.test_user, status="testing")
        stat.save()

        response = StatusMember.as_view()(
            self.get_request(method='DELETE'), pk=stat.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        stat.delete()
