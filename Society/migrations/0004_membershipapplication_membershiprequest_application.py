# Generated by Django 5.1.1 on 2024-11-16 16:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Society', '0003_remove_society_slug'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('gpa', models.DecimalField(decimal_places=2, max_digits=4)),
                ('department', models.CharField(max_length=100)),
                ('roll_number', models.CharField(max_length=20)),
                ('resume', models.FileField(blank=True, null=True, upload_to='resumes/')),
                ('reason', models.TextField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('society', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='Society.society')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='membershiprequest',
            name='application',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='membership_request', to='Society.membershipapplication'),
        ),
    ]
