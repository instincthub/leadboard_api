# Generated by Django 4.0.8 on 2022-12-23 20:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_company_username_companyinvite_invited_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyemployee',
            name='invited',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='companyemployee',
            name='role',
            field=models.CharField(blank=True, choices=[('ADMIN', 'ADMIN'), ('MARKETER', 'MARKETER')], max_length=250, null=True),
        ),
    ]
