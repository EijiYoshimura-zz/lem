from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from ..models.employee import Employee
from ..models.department import Department
import json
import re


def employee_view(request):
    """/app/employee/
    API RESTFUL for employee management
    Accepts only POST requests.
    request.body should be in JSON format:
    {
	    "action": "",
	    "id": "",
	    "name": "", 
	    "email": "",
	    "department_id": ""
    }

    action - REQUIRED
        - list - return a list of employees that match parameters
            - id            - OPTIONAL - if provided, it will ignore all other parameters and list the employee with id.
            - email         - OPTIONAL - will return the employee with informed email and ignore all other parameters.
            - name          - OPTIONAL - will find any employee that matches the string sequence (SQL LIKE). It is insensitive case.
            - department_id - OPTIONAL - will list all employees for the department
        
        - add - create a new employee registry. it will be set as active by default
            - name          - REQUIRED - String(200)
            - email         - REQUIRED - String(200) - UNIQUE
            - department_id - OPTIONAL - integer - foreign key to Department
        
        - set_active - sets the employee active
            - id - REQUIRED

        - set_inactive - sets the employee inactive
            - id - REQUIRED

        - edit - allows to edit name, email and department from employee. Can inform only the field to be edited
            - id            - REQUIRED - employee.id
            - name          - OPTIONAL
            - email         - OPTIONAL
            - department_id - OPTIONAL
    """
    if request.method == 'GET':
        return HttpResponseForbidden('GET request not allowed')

    request_body = json.loads(request.body) if request.body else {}

    action = request_body.get('action')
    id = request_body.get('id')
    name = request_body.get('name')
    email = request_body.get('email')
    department_id = request_body.get('department_id')

    if not action:
        return HttpResponseBadRequest('"action" parameter is required.')

    if action == 'list':
        if id or email:
            try:
                employee = Employee.objects.get(id=id) if id else Employee.objects.get(email=email)
            except Employee.DoesNotExist:
                return HttpResponseNotFound('Employee not found.')

            response = [{
                'id': employee.id,
                'name': employee.name,
                'email': employee.email,
                'department': employee.department.id if employee.department else None,
                'department__name': employee.department.name if employee.department else None,
                'active': employee.active
            }]

        elif name:
            query = Employee.objects.filter(name__icontains=name) \
                    .values(
                        'id', 
                        'name', 
                        'email', 
                        'department', 
                        'department__name' , 
                        'active'
                        )
            if query.count() == 0:
                return HttpResponseNotFound('Employee not found.')  

            response = list(query)                      

        elif department_id:
            try:
                department = Department.objects.get(id=department_id)
            except Department.DoesNotExist:
                return HttpResponseNotFound('Department not found.')
            
            query = Employee.objects.filter(department=department) \
                    .values(
                        'id', 
                        'name', 
                        'email', 
                        'department', 
                        'department__name' , 
                        'active'
                        )
            response = list(query)

        else:
            query = Employee.objects.all() \
                    .values(
                        'id', 
                        'name', 
                        'email', 
                        'department', 
                        'department__name' , 
                        'active'
                        )
            response = list(query)
        
    elif action == 'add':
        if not all([name,email]):
            return HttpResponseBadRequest('Data missing')

        if not re.match('[^@]+@[^@]+\.[^@]+', email):
            return HttpResponseBadRequest('Invalid email address.')

        try:
            department = Department.objects.get(id=department_id) if department_id else None
            employee = Employee(
                name=name, 
                email=email, 
                department=department,
                active=True
                )
            employee.save()

        except Department.DoesNotExist:
            return HttpResponseNotFound('Department not found.')

        except IntegrityError as exc:
            if str(exc) == 'UNIQUE constraint failed: app_person.email':
                return HttpResponseBadRequest('Employee with email {} already exists.'.format(email))
            else:
                raise exc

        response = [{
            'id': employee.id,
            'name': employee.name,
            'email': employee.email,
            'department': employee.department.id if employee.department else None,
            'department__name': employee.department.name if employee.department else None,
            'active': employee.active
        }]

    elif action == 'set_inactive' or action == 'set_active':
        if not id:
            return HttpResponseBadRequest('id is required.')

        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return HttpResponseNotFound('Employee not found.')

        employee.active = True if action == 'set_active' else False

        response = [{
            'id': employee.id,
            'name': employee.name,
            'email': employee.email,
            'department': employee.department.id if employee.department else None,
            'department__name': employee.department.name if employee.department else None,
            'active': employee.active
        }]

    elif action == 'edit':
        if not id:
            return HttpResponseBadRequest('id is required.')

        try:
            employee = Employee.objects.get(id=id)
        except Employee.DoesNotExist:
            return HttpResponseNotFound('Employee not found.')

        try:
            department = Department.objects.get(id=department_id) if department_id else None
            employee.name = name or employee.name
            employee.email = email or employee.email
            employee.department = department or employee.department

            employee.save()

        except Department.DoesNotExist:
            return HttpResponseNotFound('Department not found.')

        except IntegrityError as exc:
            if str(exc) == 'UNIQUE constraint failed: app_person.email':
                return HttpResponseBadRequest('Employee with email {} already exists.'.format(email))
            else:
                raise exc

        response = [{
            'id': employee.id,
            'name': employee.name,
            'email': employee.email,
            'department': employee.department.id if employee.department else None,
            'department__name': employee.department.name if employee.department else None,
            'active': employee.active
        }]

    else:
        return HttpResponseBadRequest('Invalid action')

    return JsonResponse(response, json_dumps_params={'indent': 2}, safe=False,)

