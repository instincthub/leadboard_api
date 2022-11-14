# Generated by Django 4.0.8 on 2022-11-07 11:58

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0007_alter_company_options_alter_group_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('nationality', models.CharField(max_length=250)),
                ('country_of_residence', models.CharField(max_length=250)),
                ('phone_number', models.CharField(max_length=50)),
                ('home_address', models.CharField(max_length=250)),
                ('experience', models.JSONField(blank=True, null=True)),
                ('education', models.JSONField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('website', models.URLField(blank=True, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('twitter', models.URLField(blank=True, null=True)),
                ('resume', models.FileField(upload_to='resumes')),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='JobSchedule',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('job_schedule', models.CharField(choices=[('REMOTE', 'REMOTE'), ('CONTRACT', 'CONTRACT'), ('FULL-TIME', 'FULL-TIME')], max_length=250, unique=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('job_type', models.CharField(choices=[('DEVELOPER', 'DEVELOPER'), ('ANIMATION', 'ANIMATION'), ('ANIMATION', 'ANIMATION'), ('DESIGN', 'DESIGN')], max_length=250)),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('applicants', models.ManyToManyField(blank=True, to='careers.applicant')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companies.company')),
                ('job_schedules', models.ManyToManyField(blank=True, to='careers.jobschedule')),
            ],
        ),
    ]