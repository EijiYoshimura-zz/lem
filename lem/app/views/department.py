from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from app.models.employee import Employee
from app.models.department import Department
import json
import re


def department_view(request):
    """/app/department/
    API RESTFUL for department management

    GET - return a list of departments that match parameters
        /app/department/                - list all departments
        /app/department/?id=00          - list department for provided id.
        /app/department/?name=xxxxx     - list all departments where name matches the string sequence (SQL LIKE). It is insensitive case.
        ?show_employees=True            - if true, will list all employees names for each department

    POST - create a new department registry. it will be set as active by default
        request.body should be in JSON format:
        {
            "name": "", 
        } 
        - name          - REQUIRED - String(200)
        
    PUT - allows to edit name and if it is active. 
        request.body should be in JSON format:
        {
            "id": "",
            "name": "",
            "active": "" 
        } 
        - id            - REQUIRED - employee.id
        - name          - OPTIONAL
        - active        - OPTIONAL
    """    

    if request.method == 'GET':
        parameters = request.GET

        id = parameters.get('id')
        name = parameters.get('name')
        show_employees = parameters.get('show_employees') == 'True' 

        if id:
            try:
                department = Department.objects.get(id=id)
            except Department.DoesNotExist:
                return HttpResponseNotFound('Department not found.')

            response = [{
                'id': department.id,
                'name': department.name,
                'active': department.active,
            }]

        elif name:
            query = Department.objects.filter(name__icontains=name) \
                    .values(
                        'id', 
                        'name', 
                        'active', 
                        )
            if query.count() == 0:
                return HttpResponseNotFound('Department not found.')  

            response = list(query)                      
            
        else:
            query = Department.objects.all() \
                    .values(
                        'id', 
                        'name', 
                        'active', 
                        )
            response = list(query)

        if show_employees:
            for i in response:
                i.update(dict(employees=list(Employee.objects.filter(department__id=i['id']).all().values('id', 'name', 'email'))))
        
    elif request.method == 'POST':
        request_body = json.loads(request.body) if request.body else {}

        name = request_body.get('name')
        if not name:
            return HttpResponseBadRequest('Data missing')

        department = Department(
            name=name, 
            active=True
            )
        department.save()

        response = [{
            'id': department.id,
            'name': department.name,
            'active': department.active
        }]


    elif request.method == 'PUT':
        request_body = json.loads(request.body) if request.body else {}

        id = request_body.get('id')
        name = request_body.get('name')
        active = request_body.get('active') if request_body.get('active') else None

        if not id:
            return HttpResponseBadRequest('id is required.')

        try:
            department = Department.objects.get(id=id)
        except Department.DoesNotExist:
            return HttpResponseNotFound('Department not found.')

        department.name = name or department.name
        department.active = (active == 'True') if active else department.active
        department.save()

        response = [{
            'id': department.id,
            'name': department.name,
            'active': department.active
        }]

    else:
        return HttpResponseBadRequest()

    return JsonResponse(
        response, 
        json_dumps_params={'indent': 2}, 
        safe=False, 
        status=(200 if request.method=='GET' else 201)
    )

