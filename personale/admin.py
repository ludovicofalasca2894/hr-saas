from django.contrib import admin
from .models import Azienda, Dipendente

@admin.register(Azienda)
class AziendaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'partita_iva', 'data_creazione')
    search_fields = ('nome', 'partita_iva')

@admin.register(Dipendente)
class DipendenteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cognome', 'azienda', 'ruolo', 'ferie_residue')
    list_filter = ('azienda', 'ruolo')
    search_fields = ('nome', 'cognome', 'email')

from .models import Profilo

@admin.register(Profilo)
class ProfiloAdmin(admin.ModelAdmin):
    list_display = ('user', 'azienda')