# Generated by Django 4.0.8 on 2022-12-02 13:34

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('object_id', models.UUIDField()),
                ('next_schedule', models.DateField(blank=True, null=True)),
                ('feedback', models.CharField(max_length=20000)),
                ('action', models.CharField(choices=[('CALL', 'CALL'), ('EMAIL', 'EMAIL'), ('SMS', 'SMS'), ('WHATSAPP', 'WHATSAPP'), ('ZOOM', 'Zoom'), ('GOOGLE-MEET', 'GOOGLE-MEET')], max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
