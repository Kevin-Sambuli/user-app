from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core import serializers
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View

from accounts.forms import AccountUpdateForm, LoginForm, RegisterForm
from accounts.models import Account

from guardian.shortcuts import assign_perm


class ActivateAccount(View):
    """
    The class view decodes the generated token from the user email during user registration and verifies the token
    If the token is valid the user instance is activated and allowed to login. 
    This is guarded by the is_active flag in the user model that is false by default and only activated when the token is validated. 
    after that the user will be redirected to the home page.
    This is to prevent users from accessing the system who dont use valid emails during registration.
    """
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
           # activating the user account to allow him to be able to log in
            user.is_active = True
            user.save()
            # return redirect('login')
            login(request, user, backend="django.contrib.auth.backends.ModelBackend")

            messages.success(
                request,
                f"Hey {user.username.title()}, Your account have been confirmed..",
            )
            subject = "WEB GIS Registration."
            message = f""" Hi {user.first_name} {user.last_name},Thank you for registering to our services.
            Please find the attached certificate of registration. """

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

            return redirect("home")
        else:
            messages.warning(
                request, "The confirmation link was invalid and the token has expired."
            )
            return redirect("home")


def registration_view(request):
    """The registration view is responsible for rendering the user registration page which has registration form
    The view supports two methods  POST and GET
    GET method is responsible for rendering the registration page
    POST method is responsible for sending the data entered in the form to the database
    
    The user is assigned to a staff group when he/she is registered successfully to allow them have some permissions
    """
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # Creating groups 
            staff_group, created = Group.objects.get_or_create(name="staff")
            admin_group, created = Group.objects.get_or_create(name="admin")
            
            
            # retrieving the aacound view model permission and assign to a group
            view_account = Permission.objects.get(codename="view_account")
            staff_group.permissions.add(view_account)
            
            # sending the user instance to the database if the form was valid
            user.save()
            
            """the user is assigned to a staff group when he/she is registered successfully to allow them have some permissions
            This is handy when control access levels to objects in the database via the admin"""
            staff_group.user_set.add(user)
            assign_perm("view_account", user, user)
            
            # Sending Success Email to the registered user
            current_site = get_current_site(request)
            subject = "Activate Your MySite Account"
            message = render_to_string(
                "accounts/account_activation_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": default_token_generator.make_token(user),
                },
            )
            user.email_user(subject, message)

            messages.info(
                request, "Please Confirm your email to complete registration."
            )

            return redirect("login")
        else:
            context["registration_form"] = form

    else:
        form = RegisterForm()
        context["registration_form"] = form
    return render(request, "accounts/register.html", context)

@login_required
def profile_view(request, *args, **kwargs):
    """This is a protected view renderes the user logged in information  and allow them to have an interaction with their data
    The view also allows the user to edit their accounts
    
    The view supports two method POST and GET
    
    POST - responsible to send the edited form to the database
    GET - Renders the profile page for the user
    
    """
    if not request.user.is_authenticated:
        return redirect("login")
    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST["email"],
                "username": request.POST["username"],
                "phone": request.POST["phone"],
                "address": request.POST["address"],
            }
            form.save()
            context["success_message"] = "Account successfully updated"
            messages.success(
                request, f" Hey ,{request.user.username}, You have edited your profile"
            )
            return redirect("home")
    else:
        # Rendering prefilled user form with their data
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
                "phone": request.user.phone,
                "address": request.user.address,
            }
        )
    context["update_form"] = form

    return render(request, "accounts/profile.html", context)


def login_view(request):
    """The login view is responsible for rendering the user login page which has login form
    The view supports two methods  POST and GET
    GET method is responsible for rendering the login page
    POST method is responsible for sending the data entered in the form to the database for authentication
    """
    context = {}

    user = request.user
    if user.is_authenticated:
        messages.success(
            request, f"Welcome back {request.user}, you have been logged in!"
        )
        return redirect("home")

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(email=email, password=password)

            if user.is_active:
                login(request, user)
                messages.success(request, f"{request.user}, Welcome back..")
                return redirect("home")
            else:
                messages.error(
                    request,
                    f"{request.user}, Your account is not activated. Please reactivate",
                )
                return redirect("login")

        else:
            messages.success(request, "Error while logging in. Please try again")
            return redirect("login")
    else:
        form = LoginForm()
    context["login_form"] = form
    return render(request, "accounts/login.html", context)


@login_required
def edit_account(request):
    """The view is responsible for allowing users to update their account"""
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST["email"],
                "username": request.POST["username"],
            }
            form.save()
            context["success_message"] = "Account successfully updated"
            messages.success(
                request, f" Hey ,{request.user.username}, You have edited your profile"
            )
            return redirect("home")
    else:
        form = AccountUpdateForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context["account_form"] = form
    return render(request, "accounts/edit_account.html", context)


def password_reset_request(request):
    """The view renderes a form that allows the user to enter their email incase they have forgotten their password
    When the form is validated an email is send to the  user to allow them to reset their password by validating the
    generated token in their email.
    
    """
    if request.method == "POST":
        pass_form = PasswordResetForm(request.POST)
        if pass_form.is_valid():
            data = pass_form.cleaned_data["email"]

            user_mail = Account.objects.filter(Q(email=data))
            
            # checks if the provided email exists in the database
            if user_mail.exists():
                current_site = get_current_site(request)
                for user in user_mail:
                    subject = "Password Request"
                    email_template_name = "accounts/password_message.txt"
                    parameters = {
                        "email": user.email,
                        "domain": current_site.domain,
                        "user": user,
                        "site_name": "Ardhi Land Info",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, parameters)
                    
                    try:
                        # sending the success email to the user
                        send_mail(subject, email, "", [user.email], fail_silently=False)
                    except:
                        return HttpResponse("Invali Header")
                    return redirect("password_reset_done")
    else:
        pass_form = PasswordResetForm(request.POST)
    context = {
        "pass_form": pass_form,
    }
    return render(request, "accounts/password_reset_form.html", context)


def update_password(request):
    """The view allows users update their password"""
    context = {}
    if request.POST:
        form = PasswordChangeForm(data=request.POST, instance=request.user.id)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "You have edited your Password")
            return redirect("home")
        else:
            messages.success(
                request, "Error while changing your password. Please try again"
            )
            return redirect("login")
    else:
        form = PasswordChangeForm(user=request.user)
    context["password_form"] = form
    return render(request, "accounts/update_password.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, f"You {request.user.username} have been logged out!")

    return redirect("home")


def webMap(request):
    """The view is renderes the leaflet map page 
    The view passes the total number of user objects from the database which is shown on the 
    leaflet legend 
    """
    
    context = {}
    users = Account.objects.all().count() # getting the total count of users in the database
    context["data"] = users
    return render(request, "map/webmap.html", context)

@login_required
def userProfiles(request):
    """This Protected view returns a HTTP response of all user objects from the database as geojson.
    The Geojson data in the response is served to the leaflet map using Jquery to display all users on the map"""
   
    # return HttpResponse(Account.objects.all(), content_type="json")
    return HttpResponse(Account.getUserData(), content_type="json")
