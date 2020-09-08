from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    # ensures html element type=password
    password = forms.CharField(widget=forms.PasswordInput)