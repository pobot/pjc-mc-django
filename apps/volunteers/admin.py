from django.contrib import admin
from django.conf import settings

from .models import *


def volunteer_compose_email_action(modeladmin, request, queryset):
    mail_to = settings.ADMIN_EMAIL
    mail_bcc = ','.join((c.email for c in queryset))
    subject = '[PJC%s] ' % settings.PJC['edition']

    import webbrowser
    webbrowser.open('mailto:?to=%s&bcc=%s&subject=%s' % (mail_to, mail_bcc, subject.replace(' ', '%20')))


volunteer_compose_email_action.short_description = "Composer un email"


@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'email', 'status', 'present']
    actions = [volunteer_compose_email_action]
    list_filter = ['status', 'present']
