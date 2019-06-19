from django.test import TestCase
from app.models.department import Department

class DepartmentTest(TestCase):
    """Test module for Department"""

    def setUp(self):
        Department.objects.create(
            name='Guitar', 
            active=True,
            )
        Department.objects.create(
            name='Vocal', 
            active=False,
            )

    def test_department(self):
        guitar = Department.objects.get(name='Guitar')
        vocal = Department.objects.get(name='Vocal')

        self.assertEqual(Department.objects.all().count(), 2)

        self.assertEqual(guitar.get_info(), 'Department: Guitar, active: True')
        self.assertEqual(vocal.get_info(), 'Department: Vocal, active: False')