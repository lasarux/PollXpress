from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User
from models import Query, Option, Person, Poll, Ballot, Space

class SpaceTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")
        self.space = Space.objects.create(
            admin=self.user, name="A Space", description="Description of this Space")

        
class PersonTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")
        self.space = Space.objects.create(
            admin=self.user, name="A Space", description="Description of this Space")
        self.person = Person.objects.create(name="User ONE", email="open@source.com")
        self.person.space.add(self.space)


class QueryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="admin")
        self.query_one = Query.objects.create(name="Query ONE", description="Description Query ONE")
        self.query_two = Query.objects.create(name="Query TWO", description="Description Query TWO")
        self.option_one = Option.objects.create(
            name="Option ONE", query=self.query_one, description="Description Query ONE")
        self.option_two = Option.objects.create(
            name="Option TWO", query=self.query_one, description="Description Query TWO")
        self.option_three = Option.objects.create(
            name="Option THREE", query=self.query_one, description="Description Query THREE")
        self.space = Space.objects.create(admin=self.user, name="Space ONE")
        self.person = Person.objects.create(name="User ONE", email="open@source.com")
        self.person.space.add(self.space)

    def testGenerateBallotsandVote(self):
        self.assertTrue(self.query_one.generate_ballots(self.space), True) 
        self.assertEqual(self.query_two.generate_ballots(), False) # with no space we can't generate ballots
        self.assertEqual(self.query_two.generate_ballots(self.space), False) # with no options we can't generate ballots
        self.assertEqual(len(self.query_one.poll_set.all()), 1) # one poll created
    
        self.assertEqual(len(mail.outbox), 1)  # Test that one message has been sent
        self.assertEqual(mail.outbox[0].subject, 'PollXpress: Query ONE - NO VOTAR AUN') # Verify that the subject of the first message is correct.

        results = self.query_one.poll_set.all()[0].result_set.all()
        for ballot in results[0].ballot_set.all():
            self.assertTrue(ballot.sent) # sent?
        
        # result before voting
        self.assertEqual(results[0].votes, 0)
        self.assertEqual(results[1].votes, 0)
        self.assertEqual(results[2].votes, 0)
        self.assertEqual(len(results), 3) # three possible results
        self.assertTrue(results[0].ballot_set.all()[0].countit())
        results = self.query_one.poll_set.all()[0].result_set.all() # refresh results
        # result after voting
        self.assertEqual(results[0].votes, 1)
        self.assertEqual(results[1].votes, 0)
        self.assertEqual(results[2].votes, 0)
        
        self.assertEqual(len(mail.outbox), 2) # check for a new mail
        self.assertEqual(mail.outbox[1].subject, 'PollXpress: Query ONE - Confirmacion del voto')
         
        for ballot in results[0].ballot_set.all():
            self.assertTrue(ballot.done) # done?
        
        # we can't vote again
        for result in results:
            self.assertFalse(result.ballot_set.all()[0].countit()) # ballots have been used
