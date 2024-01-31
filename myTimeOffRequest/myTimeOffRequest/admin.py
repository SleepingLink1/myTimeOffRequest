from django.contrib import admin
from .models import TimeOffRequest

@admin.register(TimeOffRequest)
class TimeOffRequestAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'start_date', 'end_date')
    search_fields = ('employee_id',)
