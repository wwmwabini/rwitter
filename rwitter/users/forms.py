from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

def validate_email(form_email):
    if User.objects.filter(email = form_email).exists():
        raise ValidationError((f"{form_email} is already taken."),params = {'form_email':form_email})
    
class RegisterForm(UserCreationForm):
    username = forms.CharField(min_length=2, max_length=32)
    email = forms.EmailField(validators = [validate_email])
    location = forms.CharField(max_length=150)
    dob = forms.DateField(label="Date of Birth")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'dob', 'location']