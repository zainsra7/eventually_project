from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.core.mail import send_mail, EmailMultiAlternatives

from eventually.forms import UserForm, UserProfileForm
import random

from eventually.models import UserProfile


@login_required
def index(request):
    print(request.user)
    return render(request, 'eventually/index.html', {})


def about(request):
    return HttpResponse("WHY")


def generate_random_code():
    return random.randint(100000, 999999)


def account_confirmation(request):
    if request.method == 'POST':
        ver_code = request.POST.get('ver_code')

        id = request.session['profile_id']
        password = request.session['password']
        try:
            user = User.objects.get(id=id)

            profile = UserProfile.objects.get(user=user)

            if ver_code == profile.ver_code:
                print(user.username, user.password)
                user.active = True
                user.save()
                logged_in_user = authenticate(request, username=user.username, password=user.password)
                print(logged_in_user)

                if logged_in_user:
                    if logged_in_user.is_active:
                        login(request, logged_in_user)

                        profile.approved = True
                        profile.save()
                        return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'eventually/account_confirmation.html',
                              {'error': 'Please enter a valid code. Wrong code inputted.'})
        except User.DoesNotExist:
            return HttpResponseRedirect(reverse('register'))

    return render(request, 'eventually/account_confirmation.html', {})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'eventually/login.html', {'error':'Login failed. Please check your login details'})

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

        password = request.POST.get('password')
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(password)
            request.session['password'] = password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
                profile.approved = False

            # Generate verification code and send to the user's email address
            profile.ver_code = generate_random_code()
            profile.save()
            send_mail_api(profile.user.username, profile.user.email, profile.ver_code)

            # save user profile id to session
            request.session['profile_id'] = user.id

            return HttpResponseRedirect(reverse('account_confirmation'))

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
    subject, from_email, to = 'Verification Code', 'events@eventually.com', email
    text_content = "Dear %s, \nPlease enter your verification code: %s" % (username, ver_code)
    html_content = '<strong>Let us see if this works</strong>'
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, "text/html")
    message.send()


def send_mail_forgot_password(email, ver_code):
    send_mail("Reset your password", "Please enter this code to reset to your password : %s" % ver_code,
              "events@eventually.com", [email], fail_silently=True)


# Apologies for the ambiguity between forgot_password and password reset. Forgot_password is the first page
# where users get to enter their email address. Whereas password reset is the next page where the user
# actually enters the new passcode and verification code
def forgot_password(request):
    # Possibly better option is to use a form field.
    if request.method == 'POST':
        email = request.POST.get('email')

        ver_code = generate_random_code()
        send_mail_forgot_password(email, ver_code)
        request.session["email"] = email
        try:
            user = User.objects.get(email=email)
            profile = UserProfile.objects.get(user=user)
            profile.ver_code = ver_code
            profile.save()

            return HttpResponseRedirect(reverse('password_reset'))
        except User.DoesNotExist:
            return render(request, 'eventually/forgot_password.html',
                              {'error': 'Email address is incorrect'})
        except UserProfile.DoesNotExist:
            return render(request, 'eventually/forgot_password.html',
                              {'error': 'Email address is incorrect'})

    return render(request, 'eventually/forgot_password.html', {})


def password_reset(request):
    if request.method == 'POST':
        email = request.session["email"]
        password = request.POST.get('password')
        ver_code = request.POST.get('ver_code')

        try:
            user = User.objects.get(email=email)
            profile = UserProfile.objects.get(user=user)

            if profile:
                if profile.ver_code == ver_code:
                    user.set_password(password)
                    user.save()
                    return render(request, 'eventually/index.html', {'user':user})
                else:
                    return render(request, 'eventually/forgot_password_confirmation.html',
                                  {'error': 'Verification code is incorrect'})
            else:
                return render(request, 'eventually/forgot_password_confirmation.html',
                              {'error': 'Email address is incorrect'})
        except User.DoesNotExist:
            return render(request, 'eventually/forgot_password_confirmation.html',
                              {'error': 'Email address is incorrect'})

    return render(request, 'eventually/forgot_password_confirmation.html', {})


@login_required
def sign_out(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
