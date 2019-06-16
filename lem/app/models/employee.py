from django.db import models as dbmodels
from .department import Department
from .person import Person

class Employee(Person):
    department = dbmodels.ForeignKey(Department, on_delete=dbmodels.CASCADE, blank=True, null=True)
    active = dbmodels.BooleanField(default=True)

    def __str__(self):
        return str(self.id) + ' - ' + self.name

