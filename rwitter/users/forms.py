from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import UserProfile
from django.core.exceptions import ValidationError
from bootstrap_datepicker_plus.widgets import DatePickerInput

def validate_email(form_email):
    if User.objects.filter(email = form_email).exists():
        raise ValidationError((f"{form_email} is already taken."),params = {'form_email':form_email})
    
class RegisterForm(UserCreationForm):
    username = forms.CharField(min_length=2, max_length=32)
    email = forms.EmailField(validators = [validate_email])
    location = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder':'e.g. Mamba Village, Thika, Kiambu, Kenya'}))
    dob = forms.DateField(label="Date of Birth", widget=DatePickerInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'dob', 'location']

class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'dob', 'location', 'website', 'photo']
