from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    # ensures html element type=password
    password = forms.CharField(widget=forms.PasswordInput)


# alternative to UserCreationForm
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="Password should be smart!",
                               widget=forms.PasswordInput)
    password1 = forms.CharField(label='Repeat it again',  # why password1 is not showing in the template?!
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password1(self):
        """
        clean_<fieldname>() - this type of method is invoked automatically by is_valid() and check defined validation

        this methods will validate -
        - if both password is matched or not
        - if password length is at least 8 characters
        - if password contains both numbers and letters
        """
        cd = self.cleaned_data
        if cd['password'] != cd['password1']:
            raise forms.ValidationError('Password missmatched!')
        if len(cd['password']) < 8:
            print(type(cd['password']))
            print(cd['password'])
            raise forms.ValidationError(
                'Password should be at least 8 character')
        if cd['password'].isdigit() or cd['password'].isalpha():
            raise forms.ValidationError(
                'Password should have both letters and digits!')
        return cd['password1']
