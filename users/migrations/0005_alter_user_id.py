# Generated by Django 4.0.8 on 2022-10-27 15:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default=uuid.UUID('6b5921fa-48c1-4971-8590-06749b0e0912'), editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]