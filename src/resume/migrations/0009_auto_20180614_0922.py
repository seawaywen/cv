# Generated by Django 2.0.4 on 2018-06-14 09:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0008_auto_20180614_0351'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workexperiencetranslation',
            old_name='work_experience',
            new_name='related_model',
        ),
    ]