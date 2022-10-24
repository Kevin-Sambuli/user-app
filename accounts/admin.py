from .models import Account
from .forms import RegisterForm, AccountUpdateForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin
from django.contrib import admin, messages


class AccountAdmin(OSMGeoAdmin):
    ordering = ["email"]
    add_form = RegisterForm
    # form = AccountUpdateForm
    model = Account

    list_display = ('email', 'username', 'date_joined', 'last_login', 'is_active', 'is_admin', 'is_staff')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login',)
    list_display_links = ('email',)
    filter_horizontal = ()
    list_per_page = 10
    list_filter = ('is_staff', 'is_admin', 'is_superuser', 'is_active')
    fieldsets = (
        ("Login Credentials",
         {"fields": ("email", "password",)}
         ),

        ("Personal Information",
         {"fields": ("username", "first_name", "last_name", "address","phone")}
         ),

        ("User location",
         {"fields": ("location",)}
         ),

        ("Permissions and Groups",
         {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions",)}
         ),

        ("Important Dates",
         {"fields": ("last_login", "date_joined",)}
         ),

    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "location", "is_staff", "is_active")}
         ),
    )

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True


admin.site.register(Account, AccountAdmin)
