import cloudinary
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from eventually.forms import UserForm, UserProfileForm, ProfileForm
from django.contrib.staticfiles.templatetags.staticfiles import static
from eventually.models import UserProfile
from eventually.models import Event, Attendee
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


cloudinary.config(
    cloud_name='eventually',
    api_key='398391779669939',
    api_secret='B9r_lNfKaNy2Z8bK3d9wDksxhOs'
)

##### need to sort by attendees
def index(request):
    # Fetch Popular Events from Database
    
    events = Event.objects.order_by('-date')[:5]
    context_dict = {'events': events}
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
    if request.method == 'POST':
        search = request.POST['search']
    else:
        search = ''

    event_list = Event.objects.filter(title__contains = search)

    page = request.GET.get('page', 1)
    paginator = Paginator(event_list, 5)

    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    except Event.DoesNotExist:
        events = None

    
    response = render(request, 'eventually/search.html', context={'events': events})
    return response

@login_required
def host(request):
    return HttpResponse("Host Event Page to create an event")


def event(request, event_id):
    context_dict = {}
    try:
        event = Event.objects.get(id=event_id)
        attendees = Attendee.objects.filter(event=event).count()
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            joined = Attendee.objects.filter(event=event).filter(user=user_profile)
        except:
            joined = None

        context_dict['event'] = event
        context_dict['attendees'] = attendees
        context_dict['joined'] = joined
    except:
        context_dict['event'] = None
        context_dict['attendees'] = None
        context_dict['joined'] = None

    return render(request, 'eventually/event.html', context_dict)

@login_required
def join_event(request):
    event_id = None

    if request.method == 'GET':
        event_id = request.GET['event_id']
    
    attendees = 0

    if event_id:
        event = Event.objects.get(id=int(event_id))
    
        if event:
            user_profile = UserProfile.objects.get(user=request.user)

            if user_profile:
                attendee = Attendee(event=event, user=user_profile)
                attendee.save()
                attendees = Attendee.objects.filter(event=event).count()
    
    return HttpResponse(attendees)

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
    return HttpResponse("About Us page showing information about Eventually")


def contact(request):
    return HttpResponse("Contact us page showing Team behind Eventually")
