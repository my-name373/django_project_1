from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegister, UpdateUser, UpdateProfile
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username =  form.cleaned_data.get('username')
            messages.success(request, f'successfully signed up {username}!')
            return redirect('login')
    else:
        form = UserRegister()
    return render(request, 'users/register.html', {'form':form, 'title':'register'})

@login_required
def profile(request):
    if request.method == 'POST':
        update_user = UpdateUser(request.POST, request.FILES, instance=request.user)
        update_profile = UpdateProfile(request.POST, request.FILES, instance=request.user.profile)
        if update_user.is_valid() and update_profile.is_valid():
            update_user.save()
            update_profile.save()
            messages.success(request, 'successfully updated account!')
            return redirect('profile')
    else:
        update_user = UpdateUser(instance=request.user)
        update_profile = UpdateProfile(instance=request.user.profile)

    context = {
        'update_user': update_user,
        'update_profile': update_profile,
    }
    return render(request, 'users/profile.html', context)
