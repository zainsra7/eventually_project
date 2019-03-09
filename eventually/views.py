import cloudinary
from django.http import HttpResponse
from django.shortcuts import render
from eventually.forms import UserForm, UserProfileForm
from django.contrib.staticfiles.templatetags.staticfiles import static


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


def logout(request):
    return HttpResponse("Logout")


def login(request):
    return HttpResponse("Login")


def about(request):
    return HttpResponse("About Us page showing information about Eventually")


def contact(request):
    return HttpResponse("Contact us page showing Team behind Eventually")
