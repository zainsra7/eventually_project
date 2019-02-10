from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from eventually.forms import UserForm, UserProfileForm


def index(request):
    return HttpResponse("WHY")


def about(request):
    return HttpResponse("WHY")


# sign up flow
# 1. Show user form for registeration
# 2. If user submits form, validate and return errors if there are errors
# 3. If there are no errors after submission, update user's database and send a mail to user's mail and show view for email validation

def register(request):
    if request.method == 'POST':
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

            ## If user has tried registering before, send error
            ## generate one time password, send mail and include verification code
            profile.save()

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
