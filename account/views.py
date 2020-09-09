from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm, EditUserForm, EditProfileForm
from .models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)  # storing the HTML form
        if form.is_valid():  # checks if all data are valid html input type
            cd = form.cleaned_data  # getting data from form
            # print(cd)
            user = authenticate(
                request, username=cd['username'], password=cd['password'])  # cross check the username and password with database User model. if matched, return the USer model, return none otherwise

            # If User exists in Database(user model)
            if user is not None:
                # checks if user stratus is active or not
                # but this is redundant
                # if user is not active, authenticate returns None
                # so, the else block will never execute if
                if user.is_active:
                    login(request, user)
                    message = 'Login Successful'
                else:
                    message = 'Opps! account is disabled'
            else:
                message = 'Incorrect Username or Password'

    else:
        message = None
        form = LoginForm()

    return render(request, 'account/login.html', {'form': form, 'message': message})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # creating a new User object without saving to database
            # not user_form(commit=False)
            new_user = user_form.save(commit=False)
            # setting password
            new_user.set_password(user_form.cleaned_data['password'])
            # now save the User object to database
            new_user.save()

            # create a Profile object of the User
            Profile.objects.create(user=new_user)

            return render(request, 'account/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = EditUserForm(instance=request.user,
                                 data=request.POST)
        profile_form = EditProfileForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # send an one time message to the template
            messages.success(request, 'Profile Updated succesfully')
            return redirect('account:dashboard')
        else:
            # send error message to template
            messages.error(request, 'Opps!Something goes Wrong!')
    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)

    return render(request, 'account/update_profile.html', {'user_form': user_form, 'profile_form': profile_form})
