from django.contrib import admin
from djangular_polls.models import Poll, PollItem
from django.utils.html import format_html


class PollItemInline(admin.TabularInline):
    model = PollItem

    readonly_fields = ('votes',)
    ordering = ('votes',)

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):

    inlines = (PollItemInline,)
    list_display = ('publish_date','title', 'highest_vote', 
                        'list_items', 'total_votes')

    def highest_vote(self,poll):
        try:
            return poll.poll_items().order_by('-votes')[0].text
        except IndexError:
            return "No Poll Items for this Poll"


    def list_items(self, poll):
        html = "<h3>%s</h3><ul>" % (poll.title)
        html += "\n".join("<li><strong>%s</strong> - %d</li>" % 
                          (pi.text, pi.votes) for
                               pi in poll.poll_items())
        html += "</ul>"
        return format_html(html) 

    list_items.short_description = "Poll results"
    list_items.allow_tags = True
