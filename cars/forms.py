from django import forms
from cars.models import UserProfile,Cars
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        ]


class SigninForm(forms.Form):
    username = forms.CharField(max_length=120)
    password = forms.CharField(widget=forms.PasswordInput())


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude=("user",)
        widgets = {
            "gender" : forms.Select(attrs={"class" : "form-control"})
        }

class SellCarsForm(ModelForm):
    class Meta:
        model = Cars
        exclude = ("user",)


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control"}))
    confirm_password = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

class MessagesForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
