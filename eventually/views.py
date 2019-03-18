import cloudinary
import qrcode
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from eventually.forms import ProfileForm, EventForm, EventImageForm, EventEditForm
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from eventually.models import UserProfile, Event, Attendee, Tag
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from datetime import datetime
from django.contrib.auth import update_session_auth_hash

from django.core.mail import \
    send_mail, EmailMultiAlternatives

from eventually.forms import UserForm, UserProfileForm
import random
import io

from eventually.models import UserProfile

cloudinary.config(
    cloud_name='eventually',
    api_key='398391779669939',
    api_secret='B9r_lNfKaNy2Z8bK3d9wDksxhOs'
)


# Returns top five popular events based on number of attendees
def popular_events():
    # Fetch all events from database
    events = Event.objects.all()

    # Get only five most popular events
    events = events.order_by('-attendees')[:5]

    return events


def index(request):
    profile_pic = "/static/images/pickachu.png"
    if request.user.is_authenticated():
        profile_pic = UserProfile.objects.get(user=request.user).profile_pic
    context_dict = {'events': popular_events(), "profile_pic": profile_pic}
    response = render(request, 'eventually/index.html', context=context_dict)
    return response


def dashboard(request):
    # GET requests
    search = request.GET.get('search', "")
    type_value = request.GET.get('type', "joined")
    filter_value = request.GET.get('filter', "upcoming")
    sort_value = request.GET.get('sort', "date")

    # Get current user
    user_profile = UserProfile.objects.get(user=request.user)

    # Fetch all events from database
    event_list_event = Event.objects.filter(
        Q(title__contains=search) | Q(location__contains=search) | Q(address__contains=search))
    event_tag_id = Tag.objects.filter(tag__contains=search).values_list('event', flat=True)
    event_list_tag = Event.objects.filter(id__in=event_tag_id)
    event_list = event_list_event | event_list_tag

    # Get relevant events based on selected filter
    if (filter_value == "upcoming"):
        event_filtered = event_list.filter(date__gte=datetime.now())
    elif (filter_value == "past"):
        event_filtered = event_list.filter(date__lte=datetime.now())
    else:
        event_filtered = event_list

    # Get relevant events based on selected sort
    if (sort_value == "date"):
        event_sorted = event_filtered.order_by('-date')
    else:
        event_sorted = event_filtered.order_by('-attendees')

    # Get relevant events based on selected type
    if (type_value == "joined"):
        joined = Attendee.objects.filter(user=user_profile).values_list('event', flat=True)
        event_selected = event_sorted.filter(id__in=joined)
    else:
        event_selected = event_sorted.filter(host=user_profile)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(event_selected, 9)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    except Event.DoesNotExist:
        events = None

    response = render(request, 'eventually/dashboard.html',
                      context={'events': events, 'search': search, 'type_value': type_value,
                               'filter_value': filter_value, 'sort_value': sort_value})
    return response


def search(request):
    # GET requests
    search = request.GET.get('search', "")
    filter_value = request.GET.get('filter', "upcoming")
    sort_value = request.GET.get('sort', "date")

    # Fetch all events from database
    event_list_event = Event.objects.filter(
        Q(title__contains=search) | Q(location__contains=search) | Q(address__contains=search))
    event_tag_id = Tag.objects.filter(tag__contains=search).values_list('event', flat=True)
    event_list_tag = Event.objects.filter(id__in=event_tag_id)
    event_list = event_list_event | event_list_tag

    # Get relevant events based on selected filter
    if filter_value == "upcoming":
        event_filtered = event_list.filter(date__gte=datetime.now())
    elif filter_value == "past":
        event_filtered = event_list.filter(date__lte=datetime.now())
    else:
        event_filtered = event_list

    # Get relevant events based on selected sort
    if (sort_value == "date"):
        event_sorted = event_filtered.order_by('-date')
    else:
        event_sorted = event_filtered.order_by('-attendees')

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(event_sorted, 5)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    except Event.DoesNotExist:
        events = None

    response = render(request, 'eventually/search.html',
                      context={'events': events, 'search': search, 'filter_value': filter_value,
                               'sort_value': sort_value})
    return response


# Creating the event

@login_required(login_url='register')
def host(request):
    # Successful create_event check
    event_created = False

    # To display error if the uploaded picture is not valid
    image_error = ""
    time_error = ""

    if request.method == "POST":
        date = request.POST.get('date')
        time = request.POST.get('time')
        date_time = datetime.strptime(date + " " + time, '%y/%m/%d %H:%M')
        if (datetime.now().date() == date_time.date() and datetime.now().time() >= date_time.time()):
            time_error = "Please select future time!"
            event_form = EventForm()
            event_image_form = EventImageForm()
        else:
            event_form = EventForm(data=request.POST)
            event_image_form = EventImageForm(data=request.POST)

            if event_form.is_valid() and event_image_form.is_valid():
                event = event_form.save(commit=False)  # Get Event Object
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
                    # Parsing and inserting event_date
                    if date and time:
                        event.date = datetime.strptime(date + " " + time, '%y/%m/%d %H:%M')
                    event.host = UserProfile.objects.get(user=request.user)
                    event.save()
                    return HttpResponseRedirect(reverse('event', kwargs={'event_id': event.id}))
    else:
        # Return a blank form
        event_form = EventForm()
        event_image_form = EventImageForm()
    return render(request, 'eventually/host.html',
                  {"event_form": event_form, "event_image_form": event_image_form, "image_error": image_error,
                   "event_created": event_created, 'time_error': time_error})


# Editing an event
@login_required
def edit_event(request, event_id):
    image_error = ""
    time_error = ""
    # Successful update_event check
    event_updated = False
    try:
        event = Event.objects.get(id=event_id)
        host_profile = UserProfile.objects.get(id=event.host.id)
        if host_profile.user == request.user:  # Allow editing only if the user requesting to edit event is host
            if request.method == "POST":
                date = request.POST.get('date')
                time = request.POST.get('time')
                date_time = datetime.strptime(date + " " + time, '%y/%m/%d %H:%M')
                if (datetime.now().date() == date_time.date() and datetime.now().time() >= date_time.time()):
                    time_error = "Please select future time!"
                else:
                    event_form = EventEditForm(data=request.POST)
                    event_image_form = EventImageForm(data=request.POST)

                    if event_form.is_valid() and event_image_form.is_valid():
                        event_new = event_form.save(commit=False)  # Get Event Object
                        event_updated = True
                        if 'image' in request.FILES:
                            image = request.FILES['image']
                            if '.jpg' in image.name or '.png' in image.name:
                                response = cloudinary.uploader.upload(request.FILES['image'],
                                                                      folder="event_photo/",
                                                                      public_id=event.id)
                                event.image = response['secure_url']
                            else:
                                event_updated = False
                                image_error = "Invalid Image File Type! Only .jpg and .png files supported!"
                        if event_updated:
                            event.date = date_time
                            event.description = event_new.description
                            event.fb_page = event_new.fb_page
                            event.address = event_new.address
                            event.title = event_new.title
                            event.location = event_new.location
                            event.save(update_fields=['title', 'description', 'fb_page', 'location', 'address', 'date'])
                            return HttpResponseRedirect(reverse('event', kwargs={'event_id': event.id}))

            else:
                event_form = EventEditForm(instance=event)
                event_image_form = EventImageForm()
        else:
            return HttpResponseRedirect(reverse('index'))
    except:
        return HttpResponseRedirect(reverse('index'))

    return render(request, 'eventually/edit_event.html',
                  {"event_form": event_form, "event_image_form": event_image_form, "image_error": image_error,
                   "event_updated": event_updated, 'time_error': time_error, 'event': event})


def event(request, event_id):
    context_dict = {}
    try:
        # Get event and tags based on ID
        event = Event.objects.get(id=event_id)
        tags = Tag.objects.filter(event=event)
        try:
            # Check if user has already joined event
            user_profile = UserProfile.objects.get(user=request.user)
            joined = Attendee.objects.filter(event=event).filter(user=user_profile)
        except:
            joined = None

        context_dict['event'] = event
        context_dict['joined'] = joined
        context_dict['tags'] = tags
    except:
        context_dict['event'] = None
        context_dict['joined'] = None
        context_dict['tags'] = None

    closed = (datetime.now().date() > event.date.date() and datetime.now().time() > event.date.time())
    context_dict['closed'] = closed

    return render(request, 'eventually/event.html', context_dict)


@login_required(login_url='register')
def join_event(request):
    event_id = None

    # Get event ID
    if request.method == 'GET':
        event_id = request.GET['event_id']

    if event_id:
        # Get event based on ID
        event = Event.objects.get(id=int(event_id))

        if event:
            user_profile = UserProfile.objects.get(user=request.user)

            if user_profile:
                # Add/Delete user as attendee of event in Attendee model
                try:
                    if request.GET['join_button'] == "Join event":
                        send_events_qr_code(user_profile.user.username, user_profile.user.email, event.title,
                                            event.date,
                                            event.address)
                    else:
                        send_events_qr_code_deregister(user_profile.user.username, user_profile.user.email, event.title,
                                                       event.date,
                                                       event.address)
                    attendee = Attendee(event=event, user=user_profile)
                    attendee.save()
                except:
                    Attendee.objects.filter(Q(event=event) & Q(user=user_profile)).delete()

                # Update number of attendees in Event model
                event.attendees = Attendee.objects.filter(event=event).count()
                event.save()

    return HttpResponse(event.attendees)


# Function to let users edit their profile
@login_required(login_url='register')
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
                    update_session_auth_hash(request, user)  # To validate the user's session
                    # Save user profile form date to database
                    profile.user = user
                    profile.save(update_fields=['user',
                                                'profile_pic'])  # Only update "user" and "profile_pic" fields of UserProfile instance
            except (User.DoesNotExist, UserProfile.DoesNotExist) as e:
                return HttpResponseRedirect(reverse('index'))

    else:
        # Render blank form if not HTTP POST
        user_form = ProfileForm()
        profile_form = UserProfileForm()

    # Render template depending on the context.
    return render(request, 'eventually/user_profile.html', {'user_form': user_form,
                                                            'profile_form': profile_form,
                                                            'profile_update': profile_update,
                                                            'profile_pic': profile_pic,
                                                            'image_error': image_error})


# Sign Up flow 1. Show user form for registration 2. Validate form upon submission and return errors if any 3. If
# there are no errors after submission, update user's database and send a mail to user's mail with verification code.
# Redirect to view for email validation
def register(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('index'))

    # Successful registration check
    registered = False

    # To display error if the uploaded picture is not valid
    image_error = ""

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        email_address = request.POST.get('email')

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        request.session['password'] = password

        if not email_address.endswith('gla.ac.uk'):
            return render(request, 'eventually/register.html', {'user_form': user_form,
                                                                'profile_form': profile_form,
                                                                'registered': registered,
                                                                'image_error': image_error,
                                                                'email_error': 'Email address must be a Glasgow University mail'})
        # Check if forms are valid
        elif user_form.is_valid() and profile_form.is_valid():

            # Check if email address is not taken
            try:

                user = User.objects.get(email=email_address)

                if user:
                    return render(request, 'eventually/register.html', {'user_form': user_form,
                                                                        'profile_form': profile_form,
                                                                        'registered': registered,
                                                                        'image_error': image_error,
                                                                        'email_error': 'Email address is already taken'})
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
                user.username = username

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
                    user_profile.profile_pic = static('images/pickachu.png')

                if save_profile:
                    # Generate verification code and send to the user's email address
                    user_profile.ver_code = generate_random_code()
                    send_mail_api(user_profile.user.username, user_profile.user.email, user_profile.ver_code)

                    # user.set_password(user.password)
                    user.save()
                    request.session['profile_id'] = user.id
                    request.session['email'] = user.email
                    user_profile.user = user
                    user_profile.save()

                    return HttpResponseRedirect(reverse('account_confirmation'))

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
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # Get the User object
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        if user:
            try:
                profile = UserProfile.objects.get(user=user)
            except ObjectDoesNotExist:
                return render(request, 'eventually/index.html',
                              {'error': 'Invalid Username/Password combination. Please try again!',
                               "events": popular_events()})

            if profile.approved is False:
                # save user profile id to session
                request.session['profile_id'] = user.id
                request.session['password'] = password
                return HttpResponseRedirect(reverse('account_confirmation'))
            # Is the account active? It could have been disabled
            elif user.is_active:
                # Login the User and redirect to index
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Eventually account is disabled.")
        else:
            # Bad login details were provided, So we can't log the user in
            return render(request, 'eventually/index.html',
                          {'error': 'Invalid Username/Password combination. Please try again!',
                           "events": popular_events()})

    # The request is not HTTP POST, so display the login form
    # This scenario would most likely be a HTTP GET
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object
        return render(request, 'eventually/index.html', {"events": popular_events()})


def send_mail_api(username, email, ver_code):
    subject, from_email, to = 'Verification Code', 'events@eventually.com', email
    text_content = "Dear %s, \nPlease enter your verification code: %s" % (username, ver_code)
    html_content = "Dear %s, \nPlease enter your verification code: %s <br><br>Warm Regards, <br>Evelyn from Eventually." % (
    username, ver_code)
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, "text/html")
    message.send()


def send_events_qr_code(username, email, event_name, event_date, event_venue):
    picture_title = "%s_tickets_%s.png" % (event_name, username)
    image = qrcode.make(picture_title)
    imageByteArray = io.BytesIO()
    image.save(imageByteArray, format='PNG')
    image_modified = imageByteArray.getvalue()

    subject, from_email, to = 'Ticket for %s ' % event_name, 'events@eventually.com', email
    text_content = "Dear %s, Thanks for registering. Please contact customer care for ticket" % username
    html_content = '<p>Dear %s, Thanks for registering for %s. Please find attached your special QR invitation. ' \
                   'Scan ' \
                   'this at the venue.<p> ' \
                   '<br>' \
                   '<br>' \
                   '<strong>Event details</strong> <br>' \
                   'Event Name : %s <br>' \
                   'Event Date : %s <br>' \
                   'Event Venue : %s <br> <br>Warm Regards, <br>Evelyn from Eventually.' % (
                   username, event_name, event_name, event_date, event_venue)
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, "text/html")

    message.attach(picture_title, image_modified, 'image/png')
    message.send()


def send_events_qr_code_deregister(username, email, event_name, event_date, event_venue):
    subject, from_email, to = 'Confirmation of withdrawal from event : %s ' % event_name, 'events@eventually.com', email
    text_content = "Dear %s, We are sorry to see you withdraw. " % username
    html_content = '<p>Dear %s, <br>We see that you withdrew from event : %s. We are sorry to see you go. ' \
                   '<br>' \
                   'Should you want to re-register. Please ensure to do so before the tickets are sold out.' \
                   '<br><br>Warm Regards,<br>Evelyn from Eventually.' % (username, event_name)
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, "text/html")
    message.send()


def send_mail_forgot_password(email, ver_code):
    send_mail("Reset your password",
              "Please enter this code to reset your password : %s <br><br>Warm Regards,<br>Seth from the Eventually security team." % ver_code,
              "events@eventually.com", [email], fail_silently=True)


def generate_random_code():
    return random.randint(100000, 999999)


# Function to confirm a user account through a verification code sent via email
def account_confirmation(request):
    if request.method == 'POST':
        ver_code = request.POST.get('ver_code')

        id = request.session['profile_id']
        password = request.session['password']
        try:
            user = User.objects.get(id=id)

            profile = UserProfile.objects.get(user=user)

            if ver_code == profile.ver_code:
                user.active = True
                user.save()
                logged_in_user = authenticate(request, username=user.username, password=password)

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
                    return render(request, 'eventually/index.html', {'user': user})
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


def contact(request):
    return HttpResponse("Contact us page showing Team behind Eventually")


def about(request):
    return HttpResponse("WHY")


def send_event_owner_mail(request):
    message = request.GET.get('message', None)
    to_email = request.GET.get('to_email', None)
    from_email = request.GET.get('from_email', None)

    event_title = request.GET.get('event_title', None)
    from_username = request.GET.get('username', None)

    user = User.objects.get(email=to_email)

    title = '[Eventually] New message from user %s with email address : %s' % (from_username, from_email)
    text_content = "Dear %s, \nYou have a new message from %s on the eventually platform regarding the event you created titled : %s. " \
                   "\nMeanwhile, here are the contents : \n%s \n\nYou can respond directly to the user by sending a mail to %s.  \n\n>Warm Regards, \nMatt from the Eventually messaging team." \
                   % (user, from_username, event_title,  message, from_email)

    html_content = "Dear %s, <br>You have a new message from %s on the eventually platform regarding the event you created titled : %s. " \
                   "<br> Meanwhile, here are the contents : <br>%s <br><br>You can respond directly to the user by sending a mail to %s.  <br><br>Warm Regards, <br>Matt from the Eventually messaging team." \
                   % (user, from_username, event_title, message, from_email)

    message = EmailMultiAlternatives(title, text_content, 'messages@eventually.com', [to_email])
    message.attach_alternative(html_content, "text/html")

    try:
        message.send()
        data = {
            'is_sent': True
        }
        return JsonResponse(data)
    except:
        data = {
            'is_sent': False
        }
        return JsonResponse(data)


def handler404(request):
    return render(request, 'eventually/404.html', status=404)

def handler500(request):
    return render(request, 'eventually/500.html', status=500)
