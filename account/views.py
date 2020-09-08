from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


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
