from django.test import TestCase
import unittest
from main.models import StatusReport
from payments.models import User
from django.core import serializers

class ModelTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.u = User(name="test", email="test@test.com")
        cls.u.save()

    @classmethod
    def tearDownClass(cls):
        cls.u.delete()

    def test_Status_Reports_can_be_converted_to_JSON(self):
        j = StatusReport(user=self.u, status="hello world")
        j.save()
        
        expected_json = ('[{"pk": %d, "model": "main.status_reports", "fields":'
                        ' {"status": "hello world", "user": %d, "when": "%s"}}]'
                        %(j.id, self.u.id, j.when))

        s = StatusReport.objects.get(id=j.id)
        json = serializers.serialize("json", [s])
        for new_obj in serializers.deserialize("json",json):
            self.assertEqual(new_obj.object, s)
