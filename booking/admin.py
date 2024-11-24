from django.contrib import admin
from .models import Client, Chambre, Reservation, Photo

class PhotoInline(admin.TabularInline):  # Permet d'ajouter les photos directement dans la page d'édition d'une chambre
    model = Photo
    extra = 1  # Nombre de photos supplémentaires à afficher par défaut

@admin.register(Chambre)
class ChambreAdmin(admin.ModelAdmin):
    list_display = ('numero', 'type', 'prix_par_nuit', 'statut')
    list_filter = ('type', 'statut')
    search_fields = ('numero', 'type')
    inlines = [PhotoInline]  # Ajoute les photos directement dans la page des chambres

admin.site.register(Client)
admin.site.register(Reservation)
admin.site.register(Photo)  # Permet d'ajouter des photos séparément si nécessaire
