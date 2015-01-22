from django.test import TestCase, SimpleTestCase
from djangular_polls.models import Poll, PollItem

class PollModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.jediPoll = Poll(title="Who is the best jedi")
        cls.jediPoll.save()
        cls.yoda = PollItem(poll=cls.jediPoll,
                        name="Yoda",
                        text="Yoda",
                        votes=5)
        cls.vader = PollItem(poll=cls.jediPoll,
                        name="vader",
                        text="vader",
                        votes=3)
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

    def test_reverse_relationship(self):
        self.assertEquals(self.jediPoll.poll_items().count(), 3) 
        
    def test_only_gets_correct_pollitems(self):
        newPoll = Poll(title="best villan")
        newPoll.save()

        grevious = PollItem(poll=newPoll,
                            name="grevious",
                            text="General Grevious")

        grevious.save()

        self.assertEquals(self.jediPoll.poll_items().count(), 3) 

        grevious.delete()
        newPoll.delete()

    def test_total_votes(self):
        self.assertEquals(self.jediPoll.total_votes, 8)

