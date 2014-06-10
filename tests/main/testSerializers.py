from django.test import TestCase
import unittest
from main.models import StatusReport
from payments.models import User
from main.serializers import StatusReportSerializer
from rest_framework.renderers import JSONRenderer
from collections import OrderedDict 
from rest_framework.parsers import JSONParser
from rest_framework.compat import BytesIO


class StatusReportsSerializer_Tests(TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.u = User(name="test", email="test@test.com")
        cls.u.save()

        cls.new_status = StatusReport(user=cls.u, status="hello world")
        cls.new_status.save()

        cls.expected_dict = OrderedDict([('id', cls.new_status.id), 
                         ('user',cls.u.email),
                         ('when', cls.new_status.when),
                         ('status', 'hello world'),
                                               ])
        

    @classmethod
    def tearDownClass(cls):
        cls.u.delete()
        cls.new_status.delete()
       
    def test_model_to_dictionary(self):

        serializer = StatusReportSerializer(self.new_status)

        self.assertEqual(self.expected_dict, serializer.data)

    def test_dictionary_to_json(self):
        serializer = StatusReportSerializer(self.new_status)
        content = JSONRenderer().render(serializer.data)


        expected_json = JSONRenderer().render(self.expected_dict)
        print(content)
        self.assertEqual(expected_json, content)
    

    def test_json_to_Status_Report(self):
        json = JSONRenderer().render(self.expected_dict)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)
        
        serializer = StatusReportSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(self.new_status.status, serializer.object.status)
        self.assertEqual(self.new_status.when, serializer.object.when)
        self.assertEqual(self.new_status.user, serializer.object.user)
        '''self.assertEqual(self.new_status.when.strftime("%Y-%m-%d %H:%M:%S"), 
                         serializer.object.when.strftime("%Y-%m-%d %H:%M:%S"))
        '''


