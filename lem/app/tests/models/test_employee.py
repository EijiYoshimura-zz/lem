from django.test import TestCase
from app.models.department import Department
from app.models.employee import Employee

class EmployeeTest(TestCase):
    """Test module for Employee"""

    def setUp(self):
        guitar = Department.objects.create(
            name='Guitar', 
            active=True,
            )
        vocal = Department.objects.create(
            name='Vocal', 
            active=True,
            )
        Employee.objects.create(
            name='Brian May', 
            email='brian@queen.com', 
            department=guitar,
            )
        Employee.objects.create(
            name='Elton John', 
            email='rocket@man.com', 
            department=vocal,
            )

    def test_employee(self):
        employee_brian = Employee.objects.get(name='Brian May')
        employee_elton = Employee.objects.get(name='Elton John')

        self.assertEqual(Employee.objects.all().count(), 2)

        self.assertEqual(
            employee_brian.get_info(), 
            'Employee name: Brian May, email: brian@queen.com, department: Guitar')
        self.assertEqual(
            employee_elton.get_info(), 
            'Employee name: Elton John, email: rocket@man.com, department: Vocal')