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
        cls.test_user.save()

    @classmethod
    def tearDownClass(cls):
        cls.test_user.delete()

    def get_request(self,method='GET', authed=True, user="default"):
        request_method = getattr(self.factory, method.lower())
        request = request_method("")
        if authed:
            if user == "default":
                user = self.test_user
            force_authenticate(request, user)

        return request


    def test_get_collection(self):
        statusrpt = StatusReport.objects.all()
        expected_json = StatusReportSerializer(statusrpt, many=True).data

        response = StatusCollection.as_view()(self.get_request())
        self.assertEqual(expected_json,response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
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

    def test_put_member_with_IsOwnerOrReadOnly_permissions(self):
        not_the_maker = User(id=4567, email="not@the.maker")
        response = StatusMember.as_view()(
            self.get_request(method="PUT",user=not_the_maker), pk=1)
        
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

