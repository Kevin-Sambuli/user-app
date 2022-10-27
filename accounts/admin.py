from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.admin import OSMGeoAdmin

from accounts.forms import AccountUpdateForm, RegisterForm
from accounts.models import Account

from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user


# class AccountAdmin(UserAdmin, OSMGeoAdmin):
class AccountAdmin(GuardedModelAdmin, OSMGeoAdmin):
     """ THe Custom admin inherits GuardedModalAdmin to allow objects to have object level permissions  """
    ordering = ["email"]
    add_form = RegisterForm
    form = AccountUpdateForm
    model = Account

    actions = [
        "activate_users",
    ]

    def has_module_permission(self, request):
        if super(AccountAdmin, self).has_module_permission(request):
        """ the method checks if the user has permission to a module"""
        if super().has_module_permission(request):

            return True

    def get_queryset(self, request):
        # if request.user.is_superuser:
        return super(AccountAdmin, self).get_queryset(request)
        # if request.user.is_active and request.user.is_staff:
        #     data= self.get_model_objects(request)
        #     return data

    def has_permission(self, request, obj, action):
        opts = self.opts
        code_name = f'{action}_{opts.model_name}'
        if obj:
            return request.user.has_perm(f'{opts.app_label}.{code_name}', obj)
        else:
            return True

    def has_view_permission(self, request, obj=None):
        return self.has_permission(request, obj, 'view')


    def has_delete_permission(self, request, obj=None):
        # the method checks if the user has delete permission on object
        return self.has_permission(request, obj, "delete")

    def has_change_permission(self, request, obj=None):
        """ the returns the queryset of objects the user is able to view"""
        if request.user.is_superuser:
            return self.has_permission(request, obj, 'edit')
        data = self.get_model_objects(request)
        return data

    def get_model_objects(self, request, action=None, klass=None):
        opts = self.opts
        actions = [action] if action else ["view", "edit", "delete"]
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(
            user=request.user,
            perms=[f"{perm}_{model_name}" for perm in actions],
            klass=klass
        )


    def activate_users(self, request, queryset):
        """This method allow staff users or superusers to activate a list of users at once by selecting the objects """
        cnt = queryset.filter(is_active=False).update(is_active=True)
        self.message_user(request, "Activated {} users.".format(cnt))

    activate_users.short_description = "Activate Users"

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.has_perm("auth.change_user"):
            del actions["activate_users"]
        return actions

    def get_form(self, request, obj=None, **kwargs):
        """The method overides the get form method in the UserAdmin class to have more control on what the user can access on the admin page.
            This helps Prevent non-superusers from editing their own permissions or granting other people permissions
        """
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
                "groups",
                "user_permissions",
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


admin.site.register(Account, AccountAdmin)
