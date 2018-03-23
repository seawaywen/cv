# Generated by Django 2.0.3 on 2018-03-23 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('resume', '0001_initial'), ('resume', '0002_auto_20171102_0326'), ('resume', '0003_auto_20180322_1434'), ('resume', '0004_auto_20180323_0525'), ('resume', '0005_auto_20180323_0536')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('download_link', models.CharField(max_length=255, verbose_name='Download Link')),
                ('live_link', models.CharField(max_length=255, verbose_name='Live Link')),
                ('github', models.CharField(max_length=255, verbose_name='Github')),
                ('description', models.TextField(blank=True, verbose_name='Summary')),
                ('cover_image', models.ImageField(blank=True, help_text='A 300x300 image for the project', null=True, upload_to='users/%Y/%m', verbose_name='Project Image')),
                ('is_public', models.BooleanField(default=False, verbose_name='Is this experience public ?')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkedin', models.CharField(blank=True, max_length=255, verbose_name='LinkedIn')),
                ('wechat', models.CharField(blank=True, max_length=255, verbose_name='Wechat')),
                ('facebook', models.CharField(blank=True, max_length=255, verbose_name='Facebook')),
                ('github', models.CharField(blank=True, max_length=255, verbose_name='Github')),
                ('personal_site', models.CharField(blank=True, max_length=255, verbose_name='Personal Site')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_public', models.BooleanField(default=False, verbose_name='Is this experience public?')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.UserProfile')),
            ],
        ),
        migrations.CreateModel(
            name='WorkExperienceTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en-us', 'English'), ('zh-hans', 'Chinese')], db_index=True, max_length=30, verbose_name='Language')),
                ('position', models.CharField(max_length=255, verbose_name='Job Position')),
                ('company', models.CharField(max_length=255, verbose_name='Company')),
                ('location', models.CharField(max_length=255, verbose_name='Location')),
                ('date_start', models.DateTimeField(verbose_name='Start Date')),
                ('date_end', models.DateTimeField(blank=True, null=True, verbose_name='End Date')),
                ('contribution', models.TextField(blank=True, verbose_name='Your highlight contribution')),
                ('keywords', models.TextField(blank=True, default='', help_text='The words that might search for when looking', verbose_name='Keywords')),
                ('work_experience', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='resume.WorkExperience')),
            ],
            options={
                'ordering': ('language',),
            },
        ),
        migrations.AddField(
            model_name='project',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.UserProfile'),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='Is this experience public?'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='resume.UserProfile'),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resume.UserProfile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
