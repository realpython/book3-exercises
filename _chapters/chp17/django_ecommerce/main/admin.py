from django.contrib import admin
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.forms import Textarea
from django.db import models
from embed_video.admin import AdminVideoMixin
from main.models import MarketingItem, StatusReport, Announcement, Badge


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):

    list_display = ('thumbnail', 'name', 'desc', 'users_with_badge', )

    def users_with_badge(self, badge):
        html = "<h3>Users</h3><ul>"
        html += "\n".join("<li><strong>%s</strong></li>" % (u.name) for u in
                          badge.user_set.all())
        html += "</ul>"
        return format_html(html)

    users_with_badge.short_description = "Those who are worthy"
    users_with_badge.allow_tags = True


@admin.register(Announcement)
class AnnouncementAdmin(AdminVideoMixin, admin.ModelAdmin):

    list_display = ('when', 'thumbnail', 'vid', 'info_html')

    def info_html(self, announcement):
        return format_html(announcement.info)

    info_html.short_description = "Info"
    info_html.allow_tags = True


@admin.register(MarketingItem)
class MarketingItemAdmin(admin.ModelAdmin):

    list_display = ('heading', 'live_view')

    def live_view(self, mi):
        return render_to_string("main/templatetags/circle_item.html",
                                {'marketing_items': (mi,)})

    live_view.short_description = "Rendered Template"
    live_view.allow_tags = True


@admin.register(StatusReport)
class StatusReportAdmin(admin.ModelAdmin):

    list_display = ('status', 'user', 'when')

    formfield_overrides = {
        models.CharField: {'widget': Textarea(attrs={'rows': 4, 'cols': 70})},
    }
