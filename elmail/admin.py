from django.contrib import admin
from .models import Mail

# Register your models here.


class MailAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'sender', 'date', 'recipient', 'body')
    list_display_links = ('id',)
    search_fields = ('id', 'subject', 'sender', 'recipient')
    list_filter = ('date',)


admin.site.register(Mail, MailAdmin)
