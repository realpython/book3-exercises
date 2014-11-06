from django.contrib import admin
from main.models import MarketingItem, StatusReport, Announcement, Badge
#avoid XSS vulnerabilities
from django.utils.html import format_html

admin.site.register((MarketingItem, StatusReport, Announcement, ))


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):

    list_display = ('thumbnail', 'name', 'desc', 'users_with_badge' )
    
    def users_with_badge(self, badge):
        html = "<h3>Users</h3><ul>"
        html += "\n".join("<li><strong>%s</strong></li>" % (u.name) for u in
            badge.user_set.all())
        html += "</ul>"
        return format_html(html) 

    users_with_badge.short_description = "Those who are worthy"
    users_with_badge.allow_tags = True
