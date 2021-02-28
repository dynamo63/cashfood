from django.contrib import admin
from .models import CashFoodMember, Affilie

@admin.register(CashFoodMember)
class CashFoodAdmin(admin.ModelAdmin):
    list_display = ("code", "phone_number", "username", "rugby_level","nb_affilie")

    def username(self, obj):
        try:
            return obj.user.username
        except AttributeError:
            return "Aucun"

    def nb_affilie(self, obj):
        return obj.affilie_set.count()

    nb_affilie.short_description = "Nombre d'Affilie"
    username.short_description = "Nom du Membre"

@admin.register(Affilie)
class AffilieAdmin(admin.ModelAdmin):
    list_display = ['username', 'code', 'parent']
