# Generated by Django 2.2.2 on 2019-06-15 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20190615_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='phone_number',
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
    ]
