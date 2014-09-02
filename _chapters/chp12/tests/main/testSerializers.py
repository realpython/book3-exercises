from django.test import TestCase
from main.models import StatusReport
from payments.models import User
from main.serializers import StatusReportSerializer
from rest_framework.renderers import JSONRenderer
from collections import OrderedDict
from rest_framework.parsers import JSONParser
from rest_framework.compat import BytesIO
from main.json_views import StatusCollection, StatusMember
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate


class StatusReportSerializer_Tests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.u = User(name="test", email="test@test.com")
        cls.u.save()

        cls.new_status = StatusReport(user=cls.u, status="hello world")
        cls.new_status.save()

        cls.expected_dict = OrderedDict([
            ('id', cls.new_status.id),
            ('user', cls.u.email),
            ('when', cls.new_status.when),
            ('status', 'hello world'),
        ])

    @classmethod
    def tearDownClass(cls):
        cls.u.delete()
        cls.new_status.delete()

    def test_model_to_dictionary(self):
        serializer = StatusReportSerializer(self.new_status)
        self.assertEquals(self.expected_dict, serializer.data)

    def test_dictionary_to_json(self):
        serializer = StatusReportSerializer(self.new_status)
        content = JSONRenderer().render(serializer.data)
        expected_json = JSONRenderer().render(self.expected_dict)
        self.assertEquals(expected_json, content)

    def test_json_to_StatusReport(self):

        json = JSONRenderer().render(self.expected_dict)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)

        serializer = StatusReportSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(self.new_status.status, serializer.object.status)
        import datetime
        self.assertAlmostEqual(
            self.new_status.when,
            serializer.object.when,
            delta=datetime.timedelta(seconds=1)
        )
        self.assertEqual(self.new_status.user, serializer.object.user)


class JsonViewTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.factory = APIRequestFactory()
        cls.test_user = User(email="test@test.com")
        cls.test_user.save()

    @classmethod
    def tearDownClass(cls):
        cls.test_user.delete()

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
        response = StatusCollection.as_view()(self.get_request(authed=False))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_member(self):
        status = StatusReport.objects.get(pk=1)
        expected_json = StatusReportSerializer(status).data

        response = StatusMember.as_view()(self.get_request(), pk=1)

        self.assertEqual(expected_json, response.data)

    def test_delete_member(self):
        status = StatusReport(user=self.test_user, status="testing")
        status.save()

        response = StatusMember.as_view()(
            self.get_request(method='DELETE'), pk=status.pk)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
