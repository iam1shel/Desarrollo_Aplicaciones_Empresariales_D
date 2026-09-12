from django.contrib import admin
from .models import Accesorio, AsignacionAccesorio, Equipo, FichaTecnica, Mantenimiento


class FichaTecnicaInline(admin.StackedInline):
    model = FichaTecnica
    extra = 0


class MantenimientoInline(admin.TabularInline):
    model = Mantenimiento
    extra = 0


class AsignacionAccesorioInline(admin.TabularInline):
    model = AsignacionAccesorio
    extra = 0
    fk_name = "equipo"


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "tipo", "marca", "ubicacion", "estado", "prestado_a")
    list_filter = ("estado", "tipo")
    search_fields = ("nombre", "marca", "prestado_a")
    inlines = [FichaTecnicaInline, MantenimientoInline, AsignacionAccesorioInline]


@admin.register(FichaTecnica)
class FichaTecnicaAdmin(admin.ModelAdmin):
    list_display = ("equipo", "numero_serie", "fecha_adquisicion", "garantia_hasta")


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ("equipo", "fecha", "tipo", "tecnico")
    list_filter = ("tipo",)


@admin.register(Accesorio)
class AccesorioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "tipo")


@admin.register(AsignacionAccesorio)
class AsignacionAccesorioAdmin(admin.ModelAdmin):
    list_display = ("equipo", "accesorio", "cantidad", "fecha_asignacion", "estado")
    list_filter = ("estado",)
