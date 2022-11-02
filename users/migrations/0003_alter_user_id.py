# Generated by Django 4.0.8 on 2022-10-27 15:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('1f944bc0-5cb4-4102-b972-4ffbd65ad9d1'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]