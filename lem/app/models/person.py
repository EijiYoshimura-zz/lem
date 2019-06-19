from django.db import models as dbmodels

class Person(dbmodels.Model):
    name = dbmodels.CharField('name', max_length=200, blank=False)
    email = dbmodels.CharField('email', max_length=200, blank=False, unique=True)
    created_at = dbmodels.DateTimeField(auto_now_add=True)
    updated_at = dbmodels.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_info(self):
        return 'Name: {}, email: {}'. format(self.name, self.email)