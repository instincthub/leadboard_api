# Generated by Django 4.0.8 on 2022-11-08 12:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('45cbf795-a1a1-4ce6-996d-0920a80d7244'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]
