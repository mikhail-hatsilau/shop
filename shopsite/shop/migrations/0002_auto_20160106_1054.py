# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 6, 10, 54, 1, 148563, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 13, 10, 54, 1, 148597, tzinfo=utc)),
        ),
    ]
