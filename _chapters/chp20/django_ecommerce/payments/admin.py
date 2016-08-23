from django.contrib import admin
from django.contrib.auth.models import User as DjangoUser
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'rank', 'last_4_digits', 'stripe_id')
    ordering = ('-created_at',)
    fieldsets = (
        ('User Info', {'fields': ('name', 'email', 'rank',)}),
        ('Billing', {'fields': ('stripe_id',)}),
        ('Badges', {'fields': ('badges',)}),
    )
    filter_horizontal = ('badges',)


admin.site.unregister(DjangoUser)
admin.site.unregister(Group)
admin.site.unregister(Site)
