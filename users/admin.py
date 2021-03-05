from django.contrib import admin
from .models import SBFMember, Codes

@admin.register(SBFMember)
class SBFMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'phone_number', 'parent']
    list_display_links = ['code']
    list_filter = ['parent']
    ordering = ['-user']
    exclude = ('rugby_level',)

    empty_value_display = "Aucun"
    

@admin.register(Codes)
class CodesAdmin(admin.ModelAdmin):
    list_display = ['code_parrain','sbfmember']