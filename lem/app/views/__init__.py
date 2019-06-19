from django.http import HttpResponse
from .department import department_view
from .employee import employee_view

def index(request):
    return HttpResponse(" ")