# Generated by Django 5.1.1 on 2024-11-19 16:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Society', '0005_announcement_image_announcement_is_member_specific'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='events/'),
        ),
        migrations.AddField(
            model_name='event',
            name='is_participating_event',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='max_participants',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='participants',
            field=models.ManyToManyField(blank=True, related_name='participating_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
