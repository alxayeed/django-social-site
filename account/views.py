from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm, EditUserForm, EditProfileForm
from .models import Profile, Contact
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from common.decorators import ajax_required
from actions.utils import create_action
from actions.models import Action


@login_required
def dashboard(request):
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    if following_ids:
        # if user's following others, retrieve only their actions
        actions = actions.filter(user_id_in=following_ids)
    actions = actions[:10]
    return render(request,
                  'account/dashboard.html',
                  {'section': 'dashboard',
                   'actions': actions})


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
            create_action(request.user, 'has created an account')

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


# show the user list
@login_required
def user_list(request):
    # get all active user
    users = User.objects.filter(is_active=True)
    return render(request,
                  'account/user/list.html',
                  {'users': users,
                   'section': 'people'})


# show individual user information
@login_required
def user_details(request, username):
    user = get_object_or_404(User,
                             username=username,
                             is_active=True)
    return render(request,
                  'account/user/detail.html',
                  {'user': user,
                   'section': 'people'})


# function for follow/unfollow feature
@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})
