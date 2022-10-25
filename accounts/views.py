from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
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

from .forms import AccountUpdateForm, LoginForm, RegisterForm
from .models import Account


class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = Account.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # return redirect('login')
            login(request, user)

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
    user = request.user
    if user.is_authenticated:
        return HttpResponse("You are already authenticated as " + str(user.email))

    context = {}
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

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


def profile_view(request, *args, **kwargs):
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
    if request.method == "POST":
        pass_form = PasswordResetForm(request.POST)
        if pass_form.is_valid():
            data = pass_form.cleaned_data["email"]

            user_mail = Account.objects.filter(Q(email=data))
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
    context = {}
    return render(request, "map/webmap.html", context)


def userProfiles(request):
    return HttpResponse(Account.getUserData(), content_type="json")
