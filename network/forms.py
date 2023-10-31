from django import forms
from .models import Doctor

class DoctorUpdateForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'age', 'email', 'phone_number', 'working_status', 'profession', 'country']