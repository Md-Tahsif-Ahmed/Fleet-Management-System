from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UserChangeForm, UserCreationForm

from accounts.models import User


class MyUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User number.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username','designation','phone','nid')
    list_filter = ('groups',)
    fieldsets = (
        (None, {'fields': ('username', 'password','designation', 'groups')}),
        ('Personal info', {'fields': ('address','nid', 'phone', 'email')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    search_fields = ('email','nid','username','phone','address')
    ordering = ('-id',)

admin.site.register(User, MyUserAdmin)
