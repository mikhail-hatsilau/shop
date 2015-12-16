# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
            ],
        ),
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orders',
            name='user',
        ),
        migrations.DeleteModel(
            name='Orders',
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
