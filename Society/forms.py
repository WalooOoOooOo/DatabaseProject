from django import forms
from .models import MembershipApplication
from .models import Announcement,Event

class MembershipApplicationForm(forms.ModelForm):
    class Meta:
        model = MembershipApplication
        fields = ['first_name', 'last_name', 'gpa', 'department', 'roll_number', 'resume', 'reason']
        

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'image', 'is_member_specific']
        widgets = {
            'is_member_specific': forms.CheckboxInput(),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'image', 'video', 'is_participating_event', 'max_participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }