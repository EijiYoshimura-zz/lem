from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, HttpResponseBadRequest, HttpResponseForbidden
from ..models.employee import Employee
from ..models.department import Department
import json
import re


def department_view(request):
    if request.method == 'GET':
        return HttpResponseForbidden('GET request not allowed')

    request_body = json.loads(request.body) if request.body else {}

    action = request_body.get('action')
    id = request_body.get('id')
    name = request_body.get('name')

    if not action:
        return HttpResponseBadRequest('"action" parameter is required.')

    if action == 'list':
        if id:
            try:
                department = Department.objects.get(id=id)
            except Department.DoesNotExist:
                return HttpResponseNotFound('Department not found.')

            response = [{
                'id': department.id,
                'name': department.name,
                'active': department.email,
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
        
    elif action == 'add':
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

    elif action == 'set_inactive' or action == 'set_active':
        if not id:
            return HttpResponseBadRequest('id is required.')

        try:
            department = Department.objects.get(id=id)
        except Department.DoesNotExist:
            return HttpResponseNotFound('Department not found.')

        department.active = True if action == 'set_active' else False

        response = [{
            'id': department.id,
            'name': department.name,
            'active': department.active
        }]

    elif action == 'edit':
        if not id:
            return HttpResponseBadRequest('id is required.')

        try:
            department = Department.objects.get(id=id)
        except Department.DoesNotExist:
            return HttpResponseNotFound('Department not found.')

        department.name = name or department.name

        department.save()

        response = [{
            'id': department.id,
            'name': department.name,
            'active': department.active
        }]

    else:
        raise HttpResponseBadRequest('Invalid action')

    return JsonResponse(response, json_dumps_params={'indent': 2}, safe=False,)

