from django.contrib import admin

from .models import PushDevice


class PushDeviceAdmin(admin.ModelAdmin):
    list_display = ['user', 'token']
    search_fields = ['user__username', 'user__first_name', 'user__last_name',
                     'user__email']

admin.site.register(PushDevice, PushDeviceAdmin)
