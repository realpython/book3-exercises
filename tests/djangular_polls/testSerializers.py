from django.test import TestCase, SimpleTestCase
from djangular_polls.models import Poll, PollItem
from djangular_polls.serializers import PollSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.compat import BytesIO

class PollSerializerTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.jediPoll = Poll(title="Who is the best jedi")
        cls.jediPoll.save()
        cls.yoda = PollItem(poll=cls.jediPoll,
                        name="Yoda",
                        text="Yoda")
        cls.vader = PollItem(poll=cls.jediPoll,
                        name="vader",
                        text="vader")
        cls.luke = PollItem(poll=cls.jediPoll,
                        name="Luke",
                        text="Luke")

        cls.yoda.save()
        cls.vader.save()
        cls.luke.save()

        
    @classmethod
    def tearDownClass(cls):
        cls.vader.delete()
        cls.yoda.delete()
        cls.luke.delete()
        cls.jediPoll.delete()

    def testPollSerializerIncludesPollItems(self):
        serializer = PollSerializer(self.jediPoll)
        import pprint
        pprint.pprint(serializer.data)

        #TODO: check using an OrderedDict

