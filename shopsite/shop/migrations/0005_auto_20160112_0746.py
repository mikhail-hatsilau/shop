# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20160112_0518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='from_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 12, 7, 46, 49, 768710, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='product',
            name='to_date',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 19, 7, 46, 49, 768745, tzinfo=utc)),
        ),
    ]
