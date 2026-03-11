from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, LeaveRequest, Complaint

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["phone", "address"]

class LeaveForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["reason", "from_date", "to_date"]

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["complaint_text"]
