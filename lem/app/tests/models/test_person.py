from django.test import TestCase
from app.models.person import Person

class PersonTest(TestCase):
    """Test module for Person"""

    def setUp(self):
        Person.objects.create(name='Mick Jagger', email='iammick@myemail.com')
        Person.objects.create(name='David Bowie', email='david@bowie.com')

    def test_person(self):
        person_mick = Person.objects.get(name='Mick Jagger')
        person_david = Person.objects.get(name='David Bowie')

        self.assertEqual(Person.objects.all().count(), 2)

        self.assertEqual(person_mick.get_info(), 'Name: Mick Jagger, email: iammick@myemail.com')
        self.assertEqual(person_david.get_info(), 'Name: David Bowie, email: david@bowie.com')