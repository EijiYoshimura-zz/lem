from django.db import models as dbmodels

class Person(dbmodels.Model):
    name = dbmodels.CharField('name', max_length=150, blank=False)
    email = dbmodels.CharField('email', max_length=200, blank=False)
    phone_number = dbmodels.CharField('phone number', max_length=14, blank=True)

    def __str__(self):
        return self.name

