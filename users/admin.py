from django.contrib import admin
from .models import SBFMember, Codes, Matrice, Gain, Assignement

@admin.register(SBFMember)
class SBFMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'code', 'phone_number', 'parent']
    list_display_links = ['code']
    list_filter = ['parent']
    exclude = ('rugby_level',)

    empty_value_display = "Aucun"
    

@admin.register(Codes)
class CodesAdmin(admin.ModelAdmin):
    list_display = ['code_parrain','sbfmember']

@admin.register(Matrice)
class MatriceAdmin(admin.ModelAdmin):
    list_display = ['name', 'prerequisite']
    list_display_links = ['name']
    


@admin.register(Gain)
class GainAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'matrice', 'image']
    list_filter = ['matrice']

@admin.register(Assignement)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['member', 'matrice', 'received']
    list_filter = ['matrice']
    search_fields = ['member__user__username']