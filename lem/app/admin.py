from django.contrib import admin
from .models.employee import Employee
from .models.department import Department


# Register your models here.
admin.site.register(Employee)
admin.site.register(Department)