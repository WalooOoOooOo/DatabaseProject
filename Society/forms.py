from django import forms
from .models import MembershipApplication

class MembershipApplicationForm(forms.ModelForm):
    class Meta:
        model = MembershipApplication
        fields = ['first_name', 'last_name', 'gpa', 'department', 'roll_number', 'resume', 'reason']
