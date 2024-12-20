# Generated by Django 5.1.1 on 2024-11-19 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Society', '0006_event_image_event_is_participating_event_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='video',
            field=models.FileField(blank=True, null=True, upload_to='events/videos/'),
        ),
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='events/images/'),
        ),
    ]
