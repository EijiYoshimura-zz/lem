from django.db import models as dbmodels

class Department(dbmodels.Model):
    name = dbmodels.CharField('department name', max_length=150, unique=True)
    active = dbmodels.BooleanField(default=True)

    def __str__(self):
        return self.name

