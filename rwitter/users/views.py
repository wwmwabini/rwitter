from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import RegisterForm
from .models import UserProfile 

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            location = form.cleaned_data.get('location')
            dob = form.cleaned_data.get('dob')

            user = User.objects.get(username=username)

            user_profile = UserProfile.objects.create(user=user, location=location, dob=dob)
            user_profile.save()

            return redirect('user-login')
    else:
        form = RegisterForm()
    return render(request, 'users/user_register.html', {'form': form})


def profile(request):

    user = User.objects.get(username='ray')

    context = {
        'user': user,
        'title': 'Account Profile'
    }

    return render(request, 'users/user_profile.html', context)