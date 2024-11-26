from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('Society', '0011_event_banned_participants'),
    ]

    operations = [
        migrations.RunSQL(
            """
            -- Trigger to remove a banned member from the society
            CREATE TRIGGER trigger_on_ban
            AFTER INSERT ON Society_event_banned_participants
            BEGIN
                DELETE FROM Society_society_members
                WHERE customuser_id = NEW.customuser_id
                AND society_id = (
                    SELECT society_id FROM Society_event WHERE id = NEW.event_id
                );
            END;
            """
        ),
    ]
