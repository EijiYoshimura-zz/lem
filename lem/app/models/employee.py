from django.db import models as dbmodels
from .department import Department
from .person import Person

from ..exceptions import DepartmentIsInactive

class Employee(Person):
    department = dbmodels.ForeignKey(Department, on_delete=dbmodels.CASCADE, blank=True, null=True)
    active = dbmodels.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ' - ' + self.name

    def set_department(self, department_id=None):
        if department_id:
            department = Department.objects.get(id=department_id)
            if not department.active:
                raise(DepartmentIsInactive('Department id {} is set to inactive. Cannot add employee.'.format(department.id)))
            self.department = department
        else:
            self.department = None

    @property
    def is_active(self):
        if self.department and self.department.active:
            return self.active
        else:
            return False