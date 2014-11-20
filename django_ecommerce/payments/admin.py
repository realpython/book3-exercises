from django.contrib import admin
from payments.models import User

from django.contrib.auth.models import User as DjangoUser
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

admin.site.unregister(DjangoUser)
admin.site.unregister(Group)
admin.site.unregister(Site)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'rank', 'last_4_digits', 'stripe_id')
    ordering = ('-created_at',)
    fieldsets = (
        ('User Info', {'fields': ('name', 'email', 'rank',)}),
        #('Reset Password', { 'fields' : ('password', )}),
        ('Billing', {'fields' : ('stripe_id',)}),
        ('Badges', {'fields' : ('badges',)}),
    )


