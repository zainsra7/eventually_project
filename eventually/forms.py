from django import forms
from django.contrib.auth.models import User
from eventually.models import UserProfile, Event


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, label="")

    class Meta:
        model = UserProfile
        fields = ('profile_pic',)


class ProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password',)

class EventForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="")
    
    class Meta:
        model = Event
        fields = ('title','description','location','address','capacity','image')