from django.db import models
from loginreg.models import CustomUser





class Society(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    admins = models.ManyToManyField(CustomUser, related_name='society_admins')
    members = models.ManyToManyField(CustomUser, related_name='society_members', blank=True)
    email = models.EmailField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.name

class SocietyAdmin(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)

    def __str__(self):
        return f"Admin of {self.society.name} - {self.user.username}"
    
class Announcement(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name="announcements")
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='announcements/', blank=True, null=True)  
    is_member_specific = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"Announcement: {self.title} for {self.society.name}"


class Event(models.Model):
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    venue = models.CharField(max_length=255)  
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='events/images/', blank=True, null=True)
    video = models.FileField(upload_to='events/videos/', blank=True, null=True)  
    is_participating_event = models.BooleanField(default=False)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    participants = models.ManyToManyField(CustomUser, related_name="participating_events", blank=True)

    def __str__(self):
        return f"Event: {self.title} for {self.society.name}"

    def remaining_slots(self):
        if self.is_participating_event:
            return self.max_participants - self.participants.count()
        return None


class ParticipationDetail(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participation_details')
    participant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='participation_details')
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    position = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} participating in {self.event.title}"



class MembershipApplication(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="applications")
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name="applications")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gpa = models.DecimalField(max_digits=4, decimal_places=2)
    department = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)
    reason = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Application to {self.society.name}"


class MembershipRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="membership_requests")
    society = models.ForeignKey(Society, on_delete=models.CASCADE, related_name="membership_requests")
    application = models.OneToOneField(
        'MembershipApplication', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="membership_request"
    )
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.username} to join {self.society.name} - {self.status}"


    


