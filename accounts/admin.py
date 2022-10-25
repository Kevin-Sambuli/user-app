from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin

from accounts.forms import AccountUpdateForm, RegisterForm
from accounts.models import Account


class AccountAdmin(UserAdmin, OSMGeoAdmin):
    ordering = ["email"]
    add_form = RegisterForm
    form = AccountUpdateForm
    model = Account

    actions = [
        "activate_users",
    ]

    def activate_users(self, request, queryset):
        cnt = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, "Activated {} users.".format(cnt))

    activate_users.short_description = "Activate Users"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm("auth.change_user"):
            del actions["activate_users"]
        return actions

    def has_delete_permission(self, request, obj=None):
        return False

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()

        # Prevent non-superusers from editing their own permissions
        if not is_superuser and obj is not None and obj == request.user:
            disabled_fields |= {
                "username",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups" "user_permissions",
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form

    list_display = (
        "email",
        "username",
        "date_joined",
        "last_login",
        "is_active",
        "is_admin",
        "is_staff",
    )
    search_fields = ("email", "username")
    readonly_fields = (
        "date_joined",
        "last_login",
    )
    list_display_links = ("email",)
    filter_horizontal = ()
    list_per_page = 10
    list_filter = ("is_staff", "is_admin", "is_superuser", "is_active")
    fieldsets = (
        (
            "Login Credentials",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal Information",
            {"fields": ("username", "first_name", "last_name", "address", "phone")},
        ),
        ("User location", {"fields": ("location",)}),
        (
            "Permissions and Groups",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "location",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True


admin.site.register(Account, AccountAdmin)
