from django.contrib import admin
from payments.models import User

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


