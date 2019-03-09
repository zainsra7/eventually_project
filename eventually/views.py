import cloudinary
from django.http import HttpResponse
from django.shortcuts import render
from PIL import Image
from eventually.forms import UserForm, UserProfileForm

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


def dashboard(request):
    return HttpResponse("Dashboard: Showing User's Events + Search bar/Filtering")


def search(request):
    return HttpResponse("Search Page showing all events based on search string")


def host(request):
    return HttpResponse("Host Event Page to create an event")


def event(request):
    return render(request, 'eventually/event.html', {})


def profile(request):
    return HttpResponse("Profile page to edit user profile")


def register(request):
    # Successful registration check
    registered = False

    if request.method == 'POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Check if forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save user's form data to database
            user = user_form.save()

            # Hash password and save user object
            user.set_password(user.password)
            user.save()

            # Save user profile form date to database
            profile = profile_form.save(commit=False)
            profile.user = user

            # Add profile picture to UserProfile model if provided by user
            if 'profile_pic' in request.FILES:
                # Verifying if the uploaded file is valid image (using Pillow)
                image = Image.open(request.FILES['profile_pic'])
                try:
                    image.verify()

                    # Uploading Photo to Cloudinary in "user_photo" folder with id of username
                    response = cloudinary.uploader.upload(request.FILES['profile_pic'],
                                                      folder="user_photo/",
                                                      public_id=user.username)
                    profile.profile_pic = response['secure_url']

                    # Save the UserProfile model instance
                    profile.save()

                    # Indicate that registration was successful
                    registered = True

                except Exception:
                    print('Invalid image')

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
                                                        'registered': registered})


def logout(request):
    return HttpResponse("Logout")


def login(request):
    return HttpResponse("Login")


def about(request):
    return HttpResponse("About Us page showing information about Eventually")


def contact(request):
    return HttpResponse("Contact us page showing Team behind Eventually")
