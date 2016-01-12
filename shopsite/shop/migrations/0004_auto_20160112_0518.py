# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20160106_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='product',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 12, 5, 18, 54, 657771, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 5, 18, 54, 657800, tzinfo=utc)),
        ),
    ]
