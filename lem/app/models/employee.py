from django.db import models as dbmodels
from .department import Department
from .person import Person

class Employee(Person):
    department = dbmodels.ForeignKey(Department, on_delete=dbmodels.CASCADE, blank=True, null=True)
    active = dbmodels.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ' - ' + self.name

    def set_department(self, department_id=None):
        if department_id:
            self.department = Department.objects.get(id=department_id)
        else:
            self.department = None

    def set_active(self):
        self.active = True

    def set_inactive(self):
        self.active = False

        