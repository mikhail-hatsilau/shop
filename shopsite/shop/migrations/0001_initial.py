# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('discription', models.CharField(max_length=600)),
                ('price', models.DecimalField(default=0, max_digits=8, decimal_places=2)),
                ('image', models.ImageField(default=b'static/images/default_product.png', upload_to=b'static/images')),
                ('from_date', models.DateTimeField(default=datetime.datetime(2016, 1, 12, 10, 32, 43, 521316, tzinfo=utc))),
                ('to_date', models.DateTimeField(default=datetime.datetime(2016, 1, 19, 10, 32, 43, 521352, tzinfo=utc))),
                ('category', models.ForeignKey(to='shop.Category')),
                ('seller', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ForeignKey(to='shop.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
