from django.test import TestCase
from main.models import StatusReport
from payments.models import User
from main.serializers import StatusReportSerializer
from rest_framework.renderers import JSONRenderer
from collections import OrderedDict
from rest_framework.parsers import JSONParser
from rest_framework.compat import BytesIO
from main.json_views import StatusCollection, StatusMember
import datetime


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
        self.assertAlmostEqual(
            self.new_status.when,
            serializer.object.when,
            delta=datetime.timedelta(seconds=1)
        )

        self.assertEqual(self.new_status.user, serializer.object.user)
