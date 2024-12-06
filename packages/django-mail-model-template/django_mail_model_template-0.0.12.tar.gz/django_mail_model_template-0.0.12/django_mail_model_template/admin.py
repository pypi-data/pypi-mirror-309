from django.contrib import admin
from .models import MailTemplate


class MailTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'created_at', 'updated_at')
    search_fields = ('name', 'subject')
    list_filter = ('created_at', 'updated_at')


admin.site.register(MailTemplate, MailTemplateAdmin)
