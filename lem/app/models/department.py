from django.db import models as dbmodels

class Department(dbmodels.Model):
    name = dbmodels.CharField('department name', max_length=150, unique=True)
    active = dbmodels.BooleanField(default=True)
    created_at = dbmodels.DateTimeField(auto_now_add=True)
    updated_at = dbmodels.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_info(self):
        return 'Department: {}, active: {}' \
            . format(self.name, self.active)