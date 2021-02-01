from django.contrib import admin
from django_admin_relation_links import AdminChangeLinksMixin
from .models import CashFoodMember, Affilie

@admin.register(CashFoodMember)
class CashFoodAdmin(AdminChangeLinksMixin ,admin.ModelAdmin):
    list_display = ("username", "phone_number", "code", "nb_affilie")

    def username(self, obj):
        return obj.user.username

    def nb_affilie(self, obj):
        return obj.affilie_set.count()

    nb_affilie.short_description = "Nombre d'Affilie"

@admin.register(Affilie)
class AffilieAdmin(AdminChangeLinksMixin, admin.ModelAdmin):
    list_display = ['username', 'code', 'parent']
