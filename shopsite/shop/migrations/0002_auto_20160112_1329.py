# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='from_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='to_date',
            field=models.DateTimeField(null=True),
        ),
    ]
