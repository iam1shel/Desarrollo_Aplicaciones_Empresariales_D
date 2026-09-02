from django.contrib import admin
from .models import Equipo


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "tipo", "marca", "ubicacion", "estado", "prestado_a")
    list_filter = ("estado", "tipo")
    search_fields = ("nombre", "marca", "prestado_a")
