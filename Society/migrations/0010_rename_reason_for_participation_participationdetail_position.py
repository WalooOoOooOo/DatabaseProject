# Generated by Django 5.1.1 on 2024-11-22 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Society', '0009_alter_event_venue_participationdetail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='participationdetail',
            old_name='reason_for_participation',
            new_name='position',
        ),
    ]
