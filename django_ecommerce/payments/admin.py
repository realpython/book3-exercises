from django.contrib import admin
from payments.models import User
from main.models import Badge

from django.contrib.auth.models import User as DjangoUser
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

admin.site.unregister(DjangoUser)
admin.site.unregister(Group)
admin.site.unregister(Site)

class BadgeInlineAdmin(admin.TabularInline):
    model = User.badges.through
    readonly_fields = ('name',)

    def name(self, a):
        return a.badge.name

@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = ('name', 'email', 'rank', 'last_4_digits', 'stripe_id')
    ordering = ('-created_at',)
    fieldsets = (
        ('User Info', {'fields': ('name', 'email', 'rank',)}),
        ('Billing', {'fields' : ('stripe_id',)}),
        ('Badges', {'fields' : ('badges',)}),
    )
    filter_horizontal = ('badges',)
