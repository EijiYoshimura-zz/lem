from django.db import models as dbmodels

class Person(dbmodels.Model):
    name = dbmodels.CharField('name', max_length=200, blank=False)
    email = dbmodels.CharField('email', max_length=200, blank=False, unique=True)

    def __str__(self):
        return self.name

