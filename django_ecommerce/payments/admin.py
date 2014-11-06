from django.contrib import admin
from payments.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'rank', 'last_4_digits', 'stripe_id')
    ordering = ('-created_at',)


'''
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from main.models import MyUser
from django import forms


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('extra_field1', 'extra_field2',)}),
    )

admin.site.register(MyUser, MyUserAdmin)
'''
