from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.core.mail import send_mail

from eventually.forms import UserForm, UserProfileForm
import random

from eventually.models import UserProfile


def index(request):
    print(request.user)
    return render(request, 'eventually/index.html', {})


def about(request):
    return HttpResponse("WHY")


def account_confirmation(request):
    if request.method == 'POST':
        ver_code = request.POST.get('ver_code')

        id = request.session['profile_id']
        try:
            user = User.objects.get(id=id)
            profile = UserProfile.objects.get(user=user)

            if ver_code == profile.ver_code:
                logged_in_user = authenticate(username='samuel', password='samuel1234')
                print(logged_in_user)

                if logged_in_user:
                    if logged_in_user.is_active:
                        login(request, logged_in_user)

                        profile.approved = True
                        profile.save()
                        return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'eventually/account-confirmation.html',
                               {'error': 'Please enter a valid code. Wrong code inputted.'})
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('register'))

    return render(request, 'eventually/account-confirmation.html', {})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(user)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

    return render(request, 'eventually/login.html', {})


# Sign Up flow
# 1. Show user form for registeration
# 2. Validate form upon submission and return errors if any
# 3. If there are no errors after submission, update user's database and send a mail to user's mail with verification code. Redirect to view for email validation

def register(request):
    if request.method == 'POST':
        print(request.POST)
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.set_password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.approved = False

            # Generate verification code and send to the user's email address
            activation_code = random.randint(100000, 999999)
            profile.ver_code = activation_code
            profile.save()
            send_mail_api(profile.user.username, profile.user.email, activation_code)

            # save user profile id to session
            request.session['profile_id'] = user.id

            return HttpResponseRedirect(reverse('account-confirmation'))

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'eventually/register.html', {'user_form': user_form,
                                                        'profile_form': profile_form,
                                                        })


# 1. retrieve user's details
# 2. check if user sent in confirmation code from the form
# 3. if user entered confirmation code, get code and check if database data matches the code
# 4. if database data does not match the code, send response to the user with appropriate message
# 5. if user does not exist, return appropriate message
# def validate_user_registeration(request):

def send_mail_api(username, email, ver_code):
    print(username, email, ver_code)
    send_mail("Verification code", "Dear %s, \nPlease enter your verification code: %s" % (username, ver_code),
              "events@eventually.com", [email], fail_silently=True)
