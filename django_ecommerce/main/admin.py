from django.contrib import admin
from main.models import MarketingItem, StatusReport, Announcement, Badge

admin.site.register((MarketingItem, StatusReport, Announcement, ))

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):

    list_display = ('img', 'name', 'desc')

