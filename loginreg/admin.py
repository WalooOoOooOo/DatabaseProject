from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser
from django.contrib import admin


class CustomUserCreationForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'is_superuser',)

    def clean_is_superuser(self):
        is_superuser = self.cleaned_data.get('is_superuser', False)
        if is_superuser and CustomUser.objects.filter(is_superuser=True).count() >= 2:
            raise ValidationError("You can't create more than 2 Super Admins.")
        return is_superuser

class CustomUserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm  

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            return self.add_form
        return super().get_form(request, obj, **kwargs)


admin.site.register(CustomUser, CustomUserAdmin)
