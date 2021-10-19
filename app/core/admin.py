from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "name"]  # Fields which will be displayed in the list items page
    # Fields will be display in the single item page
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    # Fields will be display in the create item page

    # The classes key sets any custom CSS classes we want to apply to the form section.
    # The fields key sets the fields you wish to display in your form.
    # In your example, the create page will allow you to set an email, password1 and password2
    add_fieldsets = ((None, {"classes": ("wide"), "fields": ("email", "password1", "password2")}),)


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
