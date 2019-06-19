from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from app.models.employee import Employee
from app.models.department import Department
import json
import re


def employee_view(request):
    """/app/employee/
    API RESTFUL for employee management

    GET - return a list of employees that match parameters
        /app/employee/                  - list all employees
        /app/employee/?id=00            - list employee for specified id
        /app/employee/?email=xxx@xx.c   - list employee with informed email
        /app/employee/?name=xxxx        - list all employees that matches the string sequence (SQL LIKE). It is insensitive case
        /app/employee/?department_id=00 - list all employees for department

    POST - create a new employee registry. it will be set as active by default
        request.body should be in JSON format:
        {
            "name": "", 
            "email": "",
            "department_id": ""
        }

        - name          - REQUIRED - String(200)
        - email         - REQUIRED - String(200) - UNIQUE
        - department_id - OPTIONAL - integer - foreign key to Department
    
    PUT - allows to edit name, email, department and if it is active. Inform only the field to be edited
        request.body should be in JSON format:
        {
            "id": "",
            "name": "", 
            "email": "",
            "department_id": "",
            "active": ""
        }

        - id            - REQUIRED - employee.id
        - name          - OPTIONAL
        - email         - OPTIONAL
        - department_id - OPTIONAL
        - active        - OPTIONAL

    """

    # if not request.body:
    #     return HttpResponseBadRequest()
    
    if request.method == 'GET':
        parameters = request.GET

        id = parameters.get('id')
        name = parameters.get('name')
        email = parameters.get('email')
        department_id = parameters.get('department_id')

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
        
    elif request.method == 'POST':
        request_body = json.loads(request.body) if request.body else {}

        id = request_body.get('id')
        name = request_body.get('name')
        email = request_body.get('email')
        department_id = request_body.get('department_id')
        active = (request_body.get('active') == 'True') if request_body.get('active') else None

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

    elif request.method == 'PUT':
        request_body = json.loads(request.body) if request.body else {}
        id = request_body.get('id')
        name = request_body.get('name')
        email = request_body.get('email')
        department_id = request_body.get('department_id')
        active = request_body.get('active') if request_body.get('active') else None

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
            employee.active = (active == 'True') if active else employee.active

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
        return HttpResponseBadRequest()

    return JsonResponse(
        response, 
        json_dumps_params={'indent': 2}, 
        safe=False, 
        status=(200 if request.method=='GET' else 201)
    )

