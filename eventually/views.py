import cloudinary
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from eventually.forms import UserForm, UserProfileForm, ProfileForm, EventForm, EventImageForm
from django.contrib.staticfiles.templatetags.staticfiles import static
from eventually.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from django.core.mail import send_mail, EmailMultiAlternatives

from eventually.forms import UserForm, UserProfileForm
import random

import io

from eventually.models import UserProfile

cloudinary.config(
    cloud_name='eventually',
    api_key='398391779669939',
    api_secret='B9r_lNfKaNy2Z8bK3d9wDksxhOs'
)


def index(request):
    # Fetch Popular Events from Database
    events = range(5)
    profile_pic = "/static/images/pickachu.png"
    if request.user.is_authenticated():
        profile_pic = UserProfile.objects.get(user=request.user).profile_pic
    context_dict = {'events': events, "profile_pic" : profile_pic}
    response = render(request, 'eventually/index.html', context=context_dict)
    return response


@login_required
def dashboard(request):
    # Fetch Popular Events from Database
    events = range(9)
    context_dict = {'events': events, }
    response = render(request, 'eventually/dashboard.html', context=context_dict)
    return response


def search(request):
    events = range(5)
    context_dict = {'events': events, }
    response = render(request, 'eventually/search.html', context=context_dict)
    return response


@login_required
def host(request):
    # Successful create_event check
    event_created = False

    # To display error if the uploaded picture is not valid
    image_error = ""

    if request.method == "POST":
        event_form = EventForm(data=request.POST)
        event_image_form = EventImageForm(data=request.POST)

        if event_form.is_valid() and event_image_form.is_valid():
            event = event_form.save(commit=False) # Get Event Object

            event_created = True

            if 'image' in request.FILES:
                image = request.FILES['image']
                if '.jpg' in image.name or '.png' in image.name:
                    response = cloudinary.uploader.upload(request.FILES['image'],
                                                        folder="event_photo/",
                                                        public_id=event.id)
                    event.image = response['secure_url']
                else:
                    event_created = False
                    image_error = "Invalid Image File Type! Only .jpg and .png files supported!"
            if event_created:
                event.host = UserProfile.objects.get(user=request.user)
                event.save()
        else:
            print(event_form.errors, event_image_form.errors)
    else:
        # Return a blank form
        event_form = EventForm()
        event_image_form = EventImageForm()
    return render(request,'eventually/host.html',{"event_form": event_form, "event_image_form" : event_image_form, "image_error": image_error, "event_created": event_created})


def event(request):
    return render(request, 'eventually/event.html', {})

@login_required
def user_profile(request):
    # Successful profile_update check
    profile_update = False

    # To display error if the uploaded picture is not valid
    image_error = ""
    profile_pic = UserProfile.objects.get(user=request.user).profile_pic

    if request.method == 'POST':

        user_form = ProfileForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Check if forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Get the current logged in User
            try:
                user = User.objects.get(username=request.user.username)
                profile = UserProfile.objects.get(user=user)

                # Save user's form data to database
                user_form_details = user_form.save(commit=False)

                profile_update = True

                if 'profile_pic' in request.FILES:
                    picture = request.FILES['profile_pic']
                    if '.jpg' in picture.name or '.png' in picture.name:
                        # Uploading Photo to Cloudinary in "user_photo" folder with id of username, it updates and replaces old version of file
                        response = cloudinary.uploader.upload(request.FILES['profile_pic'],
                                                            folder="user_photo/",
                                                            public_id=user.username)
                        profile.profile_pic = response['secure_url']
                        profile_pic = response['secure_url']
                    else:
                        profile_update = False
                        image_error = "Invalid Image File Type! Only .jpg and .png files supported!"
                if profile_update:
                    # Hash password and save user object
                    user.set_password(user_form_details.password)
                    user.save(update_fields=['password'])
                    # Save user profile form date to database
                    profile.user = user
                    profile.save(update_fields=['user','profile_pic']) # Only update "user" and "profile_pic" fields of UserProfile instance
            except (User.DoesNotExist, UserProfile.DoesNotExist) as e:
                return HttpResponseRedirect(reverse('index'))
        else:
            # Print problems to the terminal in case of invalid forms
            print(user_form.errors, profile_form.errors)
    else:
        # Render blank form if not HTTP POST
        user_form = ProfileForm()
        profile_form = UserProfileForm()

    # Render template depending on the context.
    return render(request, 'eventually/user_profile.html', {'user_form': user_form,
                                                        'profile_form': profile_form,
                                                        'profile_update': profile_update,
                                                        'image_error': image_error})


# Sign Up flow 1. Show user form for registration 2. Validate form upon submission and return errors if any 3. If
# there are no errors after submission, update user's database and send a mail to user's mail with verification code.
# Redirect to view for email validation
def register(request):
    # Successful registration check
    registered = False

    # To display error if the uploaded picture is not valid
    image_error = ""

    if request.method == 'POST':

        password = request.POST.get('password')
        email_address = request.POST.get('email')

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        request.session['password'] = password

        # Check if forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Check if email address is not taken
            try:
                users = User.objects.get(email=email_address)
            except MultipleObjectsReturned:
                return render(request, 'eventually/register.html', {'user_form': user_form,
                                                        'profile_form': profile_form,
                                                        'registered': registered,
                                                        'image_error': image_error,
                                                        'email_error': 'Email address is already taken'})
            except ObjectDoesNotExist:
                # Save user's form data to database
                user = user_form.save(commit=False)
                user.set_password(password)
                request.session['profile_id'] = user.id
                # Save user profile form date to database
                user_profile = profile_form.save(commit=False)
                user_profile.approved = False
                user_profile.user = user
                save_profile = True

                if 'profile_pic' in request.FILES:
                    picture = request.FILES['profile_pic']
                    if '.jpg' in picture.name or '.png' in picture.name:
                        # Uploading Photo to Cloudinary in "user_photo" folder with id of username
                        response = cloudinary.uploader.upload(request.FILES['profile_pic'],
                                                              folder="user_photo/",
                                                              public_id=user.username)
                        user_profile.profile_pic = response['secure_url']
                    else:
                        save_profile = False
                        image_error = "Invalid Image File Type!"
                # In Case there is no uploaded image, use default ranog one
                else:
                    user_profile.profile_pic = static('images/rango.jpg')

                if save_profile:
                    # Generate verification code and send to the user's email address
                    user_profile.ver_code = generate_random_code()
                    send_mail_api(user_profile.user.username, user_profile.user.email, user_profile.ver_code)

                    # Hash password and save user object
                    # user.set_password(user.password)
                    user.save()
                    user_profile.user = user
                    user_profile.save()

                    print('Account confirmation')
                    return HttpResponseRedirect(reverse('account_confirmation'))
        else:
            # Print problems to the terminal in case of invalid forms
            print(user_form.errors, profile_form.errors)
    else:
        # Render blank form if not HTTP POST
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render template depending on the context.
    return render(request, 'eventually/register.html', {'user_form': user_form,
                                                        'profile_form': profile_form,
                                                        'registered': registered,
                                                        'image_error': image_error})

@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed
        # to request.POST['<variable>'], because the
        # request.POST.get('<variable>') returns None if the
        # value does not exist, while request.POST['<variable>']
        # will raise a KeyError exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attemp to see if the username/password
        # combination is valid - a User object is returned if it is
        user = authenticate(username=username, password=password)

        profile = UserProfile.objects.get(user=user)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching crendentials was found
        if user:
            if profile.approved is False:
                # save user profile id to session
                request.session['profile_id'] = user.id
                request.session['password'] = password
                return HttpResponseRedirect(reverse('account_confirmation'))
            # Is the account active? It could have been disabled
            elif user.is_active:
                # If the account is valid and active, we can log the user in
                # We'll send the user back to the homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Eventually account is disabled.")
        else:
            # Bad login details were provided, So we can't log the user in
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not HTTP POST, so display the login form
    # This scenario would most likely be a HTTP GET
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object
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
                logged_in_user = authenticate(request, username=user.username, password=password)
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


def contact(request):
    return HttpResponse("Contact us page showing Team behind Eventually")
