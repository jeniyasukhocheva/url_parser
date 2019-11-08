from django.contrib import admin

from .models import ParserTask


class ParserTaskAdmin(admin.ModelAdmin):
    fieldsets = [
        ('URL to parse', {'fields': ['url']}),
        ('Timeshift', {'fields': ['minutes', 'seconds']}),
    ]
    list_display = ['url', 'start_date']
    list_filter = ['start_date']
    search_fields = ['url']


admin.site.register(ParserTask, ParserTaskAdmin)
