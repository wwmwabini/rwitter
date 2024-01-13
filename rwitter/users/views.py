from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms import RegisterForm, UpdateProfileForm, UpdateUserForm
from .models import UserProfile 

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save() #save data to user table

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

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def profile(request):

    user = User.objects.get(username=request.user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            profile_form.save()
            messages.success(request, 'Your account has been updated successfully.')
            return redirect('user-profile')
            
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.userprofile)

    context = {
        'title': 'Account Profile',
        'user': user,
        'user_form': user_form,
        'profile_form': profile_form
        
    }

    return render(request, 'users/user_profile.html', context)