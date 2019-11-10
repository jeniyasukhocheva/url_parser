from django.contrib import admin

from .models import ParserTask, UrlInfo


class ParserTaskAdmin(admin.ModelAdmin):
    add_fieldsets = [
        ('URL to parse', {'fields': ['url']}),
        ('Timeshift', {'fields': ['minutes', 'seconds']}),
    ]
    fieldsets = [
        ('URL to parse', {'fields': ['url']}),
        ('Start time', {'fields': ['start_date']}),
    ]
    readonly_fields = ['start_date']
    list_display = ['url', 'start_date']
    list_filter = ['start_date']
    search_fields = ['url']

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)


admin.site.register(ParserTask, ParserTaskAdmin)
admin.site.register(UrlInfo)
