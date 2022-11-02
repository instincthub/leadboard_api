# Generated by Django 4.0.8 on 2022-10-27 15:57

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_rename_company_group_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
