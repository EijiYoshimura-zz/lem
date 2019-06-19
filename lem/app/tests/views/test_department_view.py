import json
from django.test import TestCase, Client
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from app.models.employee import Employee
from app.models.department import Department

# initialize the APIClient app
client = Client()

class GetAllDepartmentTest(TestCase):
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

    def test_get_all_departments(self):
        # get API response
        response = client.get(reverse('department'))

        # get data from db
        departments = Department.objects.all() \
                        .values(
                            'id', 
                            'name', 
                            'active', 
                        )
        result = list(departments)

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)

    def test_get_all_departments_with_employees(self):
        # get API response
        response = client.get(
            reverse('department'),
            {'show_employees': True}
        )

        # get data from db
        departments = Department.objects.all() \
                        .values(
                            'id', 
                            'name', 
                            'active', 
                        )
        result = list(departments)

        for i in result:
            i.update(dict(employees=list(
                Employee.objects.filter(department__id=i['id']).all() \
                    .values('id', 'name', 'email'))))

        self.assertEqual(response.json(), result)
        self.assertEqual(response.status_code, 200)


class GetSelectedDepartmentTest(TestCase):
    """ Test module for GET single puppy API """

    def setUp(self):
        self.rock = Department.objects.create(name='Rock')
        self.folk = Department.objects.create(name='Folk')
        self.folk_rock = Department.objects.create(name='Folk Rock')

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
            department=self.folk_rock,
            )

    def test_get_valid_department_by_id(self):
        # import pdb; pdb.set_trace()
        response = client.get(
            reverse('department'), 
            {'id': self.rock.id},
            )
        department = Department.objects.filter(id=self.rock.id) \
            .values(
                'id', 
                'name', 
                'active'
            )

        self.assertEqual(response.json(), list(department))
        self.assertEqual(response.status_code, 200)

    def test_get_valid_department_by_name(self):
        # import pdb; pdb.set_trace()
        response = client.get(
            reverse('department'), 
            {'name': 'folk'},
            )
        departments = Department.objects \
            .filter(id__in=[self.folk.id, self.folk_rock.id]) \
            .values('id', 'name', 'active')

        self.assertEqual(len(response.json()), 2)
        self.assertEqual(response.json(), list(departments))
        self.assertEqual(response.status_code, 200)    

    def test_get_invalid_department(self):
        response = client.get(
            reverse('department'), {'id': 30})
        self.assertEqual(response.status_code, 404)
        
    def test_get_invalid_name_department(self):
        response = client.get(
            reverse('department'), {'name': 'forro'})
        self.assertEqual(response.status_code, 404)

class CreateNewDepartmentTest(TestCase):
    """ Test module for inserting a new department """

    def setUp(self):

        self.valid_payload = {
            'name':'Tester Developers', 
        }
        self.invalid_payload = {
            'name':'', 
        }

    def test_create_valid_department(self):
        response = client.post(
            reverse('department'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)

    def test_create_invalid_department(self):
        response = client.post(
            reverse('department'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)

class EditDepartmentTest(TestCase):
    """ Test module for editing an department """

    def setUp(self):
        self.rock = Department.objects.create(name='Rock')
        self.folk = Department.objects.create(name='Folk', active=False)
        
    def test_edit_department_name(self):
        response = client.put(
            reverse('department'),
            data=json.dumps({'id': self.rock.id, 'name': 'Rock\'n Roll'})
        )

        rock = Department.objects.get(id=self.rock.id)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(rock.name, 'Rock\'n Roll')

    def test_edit_department_active_false(self):
        response = client.put(
            reverse('department'),
            data=json.dumps({'id': self.rock.id, 'active': 'False'})
        )

        rock = Department.objects.get(id=self.rock.id)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(rock.active, False)

    def test_edit_department_active_true(self):
        response = client.put(
            reverse('department'),
            data=json.dumps({'id': self.folk.id, 'active': 'True'})
        )

        folk = Department.objects.get(id=self.folk.id)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(folk.active, True)


    def test_edit_without_id(self):
        response = client.put(
            reverse('department'),
            data=json.dumps({'id': '', 'active': 'True'})
        )

        self.assertEqual(response.status_code, 400)
