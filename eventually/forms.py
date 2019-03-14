from django import forms
from django.contrib.auth.models import User
from eventually.models import UserProfile, Event
import datetime
import re


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    profile_pic = forms.ImageField(required=False, label="", widget=forms.FileInput(attrs={"accept": "image/*"}))

    class Meta:
        model = UserProfile
        fields = ('profile_pic',)


class ProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('password',)
    

class EventImageForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="", widget=forms.FileInput(attrs={"accept": "image/*"}))

    class Meta:
        model = Event
        fields = ('image',)

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': "datepicker"}))
    post_code = forms.CharField(widget=forms.TextInput(attrs={'size': 8, 'maxLength': 8}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'timepicker'}))
    fb_page = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Write down the name of your Facebook Page', 'class': "validate"}), label="Facebook Page")

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < datetime.date.today():
            raise forms.ValidationError("The date cannot be in past!")
        return date

    def clean_post_code(self):
        post_code = self.cleaned_data['post_code']
        gov_postcode = "([Gg][Ii][Rr] 0[Aa]{2})|((([A-Za-z][0-9]{1,2})|(([A-Za-z][A-Ha-hJ-Yj-y][0-9]{1,2})|(([A-Za-z][0-9][A-Za-z])|([A-Za-z][A-Ha-hJ-Yj-y][0-9][A-Za-z]?))))\s?[0-9][A-Za-z]{2})"
        if not re.search(gov_postcode, post_code):
            raise forms.ValidationError("Invalid PostCode!")
        return post_code
        
    class Meta:
        model = Event
        fields = ('title','description','date','time','post_code','address','capacity','fb_page')