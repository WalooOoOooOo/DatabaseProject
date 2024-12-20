from django import forms
from .models import MembershipApplication
from .models import Announcement,Event,ParticipationDetail
from loginreg.models import CustomUser


class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['profile_picture']

class ParticipationDetailForm(forms.ModelForm):
    class Meta:
        model = ParticipationDetail
        fields = ['name', 'age', 'position']
        
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
        fields = ['title', 'description', 'date', 'venue', 'image', 'video', 'is_participating_event', 'max_participants']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }