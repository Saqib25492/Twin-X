# Generated by Django 4.2.4 on 2023-08-06 10:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_book', '0007_followerscount_alter_post_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 6, 15, 48, 20, 972962)),
        ),
    ]