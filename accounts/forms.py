from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Account


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput())
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput())
    username = forms.CharField(label="", max_length=100, widget=forms.TextInput())
    address = forms.CharField(label="", max_length=50, widget=forms.TextInput())
    email = forms.EmailField(label="", max_length=100, widget=forms.TextInput())
    phone = forms.CharField(label="", max_length=15, widget=forms.TextInput())
    password1 = forms.CharField(label="", widget=forms.PasswordInput())
    password2 = forms.CharField(label="", widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "phone",
            "address",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["placeholder"] = "First Name"
        self.fields["first_name"].label = ""

        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["placeholder"] = "Last Name"
        self.fields["last_name"].label = ""

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["email"].label = ""

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["placeholder"] = "User Name"
        self.fields["username"].label = ""

        self.fields["address"].widget.attrs["class"] = "form-control"
        self.fields["address"].widget.attrs["placeholder"] = "Address"
        self.fields["address"].label = ""

        self.fields["phone"].widget.attrs["class"] = "form-control"
        self.fields["phone"].widget.attrs["placeholder"] = "Phone Number"
        self.fields["phone"].label = ""

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password1"].label = ""

        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["placeholder"] = "Confirm Password"
        self.fields["password2"].label = ""

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(
                username=username
            )
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


class LoginForm(forms.ModelForm):
    email = forms.EmailField(label="", max_length=100, widget=forms.TextInput())
    password = forms.CharField(label="", widget=forms.PasswordInput)
    # remember = forms.BooleanField(label="Remember Me", required=False)

    class Meta:
        model = Account
        fields = ("email", "password")

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["placeholder"] = "Enter valid email"
        self.fields["email"].label = ""

        self.fields["password"].widget.attrs["class"] = "form-control"
        self.fields["password"].widget.attrs["placeholder"] = "Password"
        self.fields["password"].label = ""

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login credentials")


class AccountUpdateForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.TextInput(attrs={'type': 'hidden'}))

    class Meta:
        model = Account
        fields = ("email", "username", "phone", "address")

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(
                username=username
            )
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data["username"]
        account.email = self.cleaned_data["email"].lower()
        if commit:
            account.save()
        return account
