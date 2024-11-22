# Generated by Django 5.1.1 on 2024-11-22 13:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Society', '0008_event_venue'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.CharField(max_length=255),
        ),
        migrations.CreateModel(
            name='ParticipationDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('age', models.PositiveIntegerField()),
                ('reason_for_participation', models.TextField()),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participation_details', to='Society.event')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participation_details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
