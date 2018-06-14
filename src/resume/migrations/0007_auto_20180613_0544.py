# Generated by Django 2.0.4 on 2018-06-13 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0006_auto_20180413_0235'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperiencetranslation',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('zh-hans', 'Chinese')], db_index=True, max_length=30, verbose_name='Language'),
        ),
    ]