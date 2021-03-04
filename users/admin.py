from django.contrib import admin
from .models import SBFMember

@admin.register(SBFMember)
class SBFMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'phone_number']
    list_display_links = ['code']
    