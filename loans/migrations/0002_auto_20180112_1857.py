# Generated by Django 2.0.1 on 2018-01-12 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loan',
            old_name='turn',
            new_name='term',
        ),
    ]