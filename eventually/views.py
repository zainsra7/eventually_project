import cloudinary
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from eventually.forms import UserForm, UserProfileForm, ProfileForm
from django.contrib.staticfiles.templatetags.staticfiles import static
from eventually.models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


cloudinary.config(
    cloud_name='eventually',
    api_key='398391779669939',
    api_secret='B9r_lNfKaNy2Z8bK3d9wDksxhOs'
)


def index(request):
    # Fetch Popular Events from Database
    events = range(5)
    context_dict = {'events': events, }
    response = render(request, 'eventually/index.html', context=context_dict)
    return response

@login_required
def dashboard(request):
    #Fetch Popular Events from Database
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
    return HttpResponse("Host Event Page to create an event")


def event(request):
    return render(request, 'eventually/event.html', {})

@login_required
def profile(request):
    # Successful profile_update check
    profile_update = False

    # To display error if the uploaded picture is not valid
    image_error = ""

    if request.method == 'POST':

        user_form = ProfileForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Check if forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Get the current logged in User
            user = User.objects.get(username=request.user.username)
            user_profile = UserProfile.objects.get(user=user)

            # Save user's form data to database
            user_form_details = user_form.save(commit=False)

            profile_update = True

            if 'profile_pic' in request.FILES:
                picture = request.FILES['profile_pic']
                if '.jpg' in picture.name or '.png' in picture.name:
                    # Uploading Photo to Cloudinary in "user_photo" folder with id of username
                    response = cloudinary.uploader.upload(request.FILES['profile_pic'],
                                                    folder="user_photo/",
                                                    public_id=user.username)
                    user_profile.profile_pic = response['secure_url']
                else:
                    profile_update = False
                    image_error = "Invalid Image File Type!"

            if profile_update:
                # Hash password and save user object
                user.set_password(user_form_details.password)
                user.save(update_fields=['password'])
                # Save user profile form date to database
                user_profile.user = user
                user_profile.save(update_fields=['user', 'profile_pic'])
                profile_update = True # Indicate that profile  was updated successfully
        else:
            # Print problems to the terminal in case of invalid forms
            print(user_form.errors, profile_form.errors)
    else:
        # Render blank form if not HTTP POST
        user_form = ProfileForm()
        profile_form = UserProfileForm()

    # Render template depending on the context.
    return render(request, 'eventually/profile.html', {'user_form': user_form,
                                                        'profile_form': profile_form,
                                                        'profile_update': profile_update,
                                                        'image_error': image_error})

def register(request):
    # Successful registration check
    registered = False

    # To display error if the uploaded picture is not valid
    image_error = ""

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Check if forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save user's form data to database
            user = user_form.save(commit=False)

            # Save user profile form date to database
            user_profile = profile_form.save(commit=False)
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
                # Hash password and save user object
                user.set_password(user.password)
                user.save()
                user_profile.user = user
                user_profile.save()
                registered = True # Indicate that Registration was successful
                return HttpResponseRedirect(reverse('index'))
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

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching crendentials was found
        if user:
            # Is the account active? It could have been disabled
            if user.is_active:
                # If the account is valid and active, we can log the user in
                # We'll send the user back to the homepage
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Eventually account is disabled.")
        else:
            # Bad login details were provided, So we can't log the user in
            print("Invalid login details: {0}, {1}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    # The request is not HTTP POST, so display the login form
    # This scenario would most likely be a HTTP GET
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object
        return render(request,'eventually/index.html', {})

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


# Sign Up flow 1. Show user form for registeration 2. Validate form upon submission and return errors if any 3. If
# there are no errors after submission, update user's database and send a mail to user's mail with verification code.
# Redirect to view for email validation
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


def contact(request):
    return HttpResponse("Contact us page showing Team behind Eventually")


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
