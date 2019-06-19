import json
from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from app.models.employee import Employee
from app.models.department import Department

# initialize the APIClient app
client = Client()

class GetAllEmployeesTest(TestCase):
    """ Test module for GET all employees API """

    def setUp(self):
        rock = Department.objects.create(name='Rock')
        folk = Department.objects.create(name='Folk')
        soul = Department.objects.create(name='Soul')

        Employee.objects.create(
            name='Bryan Adams', 
            email='bryan_adams@myemail.com',
            department=rock,
            )
        Employee.objects.create(
            name='James Brown',
            email='james@brown.com',
            department=folk,
            )
        Employee.objects.create(
            name='Jack Johnson', 
            email='jack@beach.com',
            department=soul,
            )

    def test_get_all_employees(self):
        # get API response
        response = client.get(reverse('employee'))

        # get data from db
        employees = Employee.objects.all() \
                        .values(
                            'id', 
                            'name', 
                            'email', 
                            'department', 
                            'department__name' , 
                            'active'
                        )
        result = list(employees)

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)


class GetSelectedEmployeeTest(TestCase):
    """ Test module for GET single puppy API """

    def setUp(self):
        self.rock = Department.objects.create(name='Rock')
        self.folk = Department.objects.create(name='Folk')
        self.soul = Department.objects.create(name='Soul')

        self.brian = Employee.objects.create(
            name='Bryan Adams', 
            email='bryan_adams@myemail.com',
            department=self.rock,
            )
        self.james = Employee.objects.create(
            name='James Brown',
            email='james@brown.com',
            department=self.folk,
            )
        self.blunt = Employee.objects.create(
            name='James Blunt',
            email='james@blunt.com',
            department=self.folk,
            )
        self.jack = Employee.objects.create(
            name='Jack Johnson', 
            email='jack@beach.com',
            department=self.soul,
            )

    def test_get_valid_employee_by_id(self):
        # import pdb; pdb.set_trace()
        response = client.get(
            reverse('employee'), 
            {'id': self.james.id},
            )
        employee = Employee.objects.filter(id=self.james.id) \
            .values(
                'id', 
                'name', 
                'email', 
                'department', 
                'department__name' , 
                'active'
            )

        self.assertEqual(response.json(), list(employee))
        self.assertEqual(response.status_code, 200)

    def test_get_valid_employee_by_name(self):
        # import pdb; pdb.set_trace()
        response = client.get(
            reverse('employee'), 
            {'name': 'james'},
            )
        employee = Employee.objects.filter(id__in=[self.james.id, self.blunt.id]) \
            .values(
                'id', 
                'name', 
                'email', 
                'department', 
                'department__name' , 
                'active'
            )

        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json(), list(employee))
        self.assertEqual(response.status_code, 200)    

    def test_get_valid_employee_by_email(self):
            # import pdb; pdb.set_trace()
        response = client.get(
            reverse('employee'), 
            {'email': 'jack@beach.com'},
            )
        employee = Employee.objects.filter(id=self.jack.id) \
            .values(
                'id', 
                'name', 
                'email', 
                'department', 
                'department__name' , 
                'active'
            )

        self.assertEqual(response.json(), list(employee))
        self.assertEqual(response.status_code, 200)    

    def test_get_valid_employee_by_department(self):
            # import pdb; pdb.set_trace()
        response = client.get(
            reverse('employee'), 
            {'department_id': self.folk.id},
            )
        employee = Employee.objects.filter(department__id=self.folk.id) \
            .values(
                'id', 
                'name', 
                'email', 
                'department', 
                'department__name' , 
                'active'
            )

        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json(), list(employee))
        self.assertEqual(response.status_code, 200)   

    def test_get_invalid_employee(self):
        response = client.get(
            reverse('employee'), {'id': 30})
        self.assertEqual(response.status_code, 404)
        
    def test_get_invalid_department(self):
        response = client.get(
            reverse('employee'), {'department_id': 30})
        self.assertEqual(response.status_code, 404)

class CreateNewEmployeeTest(TestCase):
    """ Test module for inserting a new employee """

    def setUp(self):
        self.rock = Department.objects.create(name='Rock')

        Employee.objects.create(
            name='James Brown',
            email='james@brown.com',
            department=self.rock,
            )

        self.valid_payload = {
            'name':'Bryan Adams', 
            'email':'bryan_adams@myemail.com',
            'department_id':self.rock.id,
        }
        self.invalid_payload = {
            'name':'Jack Johnson', 
            'email':'',
            'department_id':None,
        }
        self.unique_email_payload = {
            'name': 'J. Brown', 
            'email': 'james@brown.com'
        }

    def test_create_valid_employee(self):
        response = client.post(
            reverse('employee'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_employee(self):
        response = client.post(
            reverse('employee'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

    def test_create_employee_invalid_unique_email(self):
        response = client.post(
            reverse('employee'),
            data=json.dumps(self.unique_email_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
       

class EditEmployeeTest(TestCase):
    """ Test module for editing an employee """

    def setUp(self):
        self.rock = Department.objects.create(name='Rock')
        self.folk = Department.objects.create(name='Folk')
        self.soul = Department.objects.create(name='Soul')

        self.brian = Employee.objects.create(
            name='Bryan Adams', 
            email='bryan_adams@myemail.com',
            department=self.rock,
            )
        self.blunt = Employee.objects.create(
            name='James Blunt',
            email='james@blunt.com',
            department=self.folk,
            )
        self.jack = Employee.objects.create(
            name='Jack Johnson', 
            email='jack@beach.com',
            department=self.soul,
            active=False,
            )
        
    def test_edit_employee_email(self):
        response = client.put(
            reverse('employee'),
            data=json.dumps({'id': self.jack.id, 'email': 'jack_johnson@beach.com'})
        )

        jack = Employee.objects.get(id=self.jack.id)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(jack.email, 'jack_johnson@beach.com')

    def test_edit_employee_name(self):
        response = client.put(
            reverse('employee'),
            data=json.dumps({'id': self.brian.id, 'name': 'Brian Adao'})
        )

        brian = Employee.objects.get(id=self.brian.id)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(brian.name, 'Brian Adao')

    def test_edit_employee_active_false(self):
        response = client.put(
            reverse('employee'),
            data=json.dumps({'id': self.brian.id, 'active': 'False'})
        )

        brian = Employee.objects.get(id=self.brian.id)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(brian.active, False)

    def test_edit_employee_active_true(self):
        response = client.put(
            reverse('employee'),
            data=json.dumps({'id': self.jack.id, 'active': 'True'})
        )

        jack = Employee.objects.get(id=self.jack.id)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(jack.active, True)

    def test_edit_employee_department(self):
        response = client.put(
            reverse('employee'),
            data=json.dumps({'id': self.blunt.id, 'department_id': self.soul.id})
        )
        
        blunt = Employee.objects.get(id=self.blunt.id)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(blunt.department, self.soul)

