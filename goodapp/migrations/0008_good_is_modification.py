# Generated by Django 3.1 on 2020-09-17 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goodapp', '0007_good_parent_good'),
    ]

    operations = [
        migrations.AddField(
            model_name='good',
            name='is_modification',
            field=models.BooleanField(default=False, verbose_name='Модификация'),
        ),
    ]
