from django.contrib import admin
from .models import (
    AutorizacionEspacio,
    Categoria,
    DetallePrestamo,
    Espacio,
    PerfilSolicitante,
    Prestamo,
    Solicitante,
)


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "edificio", "piso", "aforo")
    search_fields = ("nombre", "edificio")


class PerfilSolicitanteInline(admin.StackedInline):
    model = PerfilSolicitante
    extra = 0


class AutorizacionEspacioInline(admin.TabularInline):
    model = AutorizacionEspacio
    extra = 0
    fk_name = "solicitante"


@admin.register(Solicitante)
class SolicitanteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "codigo", "rol", "correo")
    list_filter = ("rol",)
    search_fields = ("nombre", "codigo")
    inlines = [PerfilSolicitanteInline, AutorizacionEspacioInline]


class DetallePrestamoInline(admin.TabularInline):
    model = DetallePrestamo
    extra = 1


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre_solicitante",
        "fecha_prestamo",
        "fecha_estimada_devolucion",
        "estado",
    )
    list_filter = ("estado",)
    search_fields = ("codigo", "nombre_solicitante")
    inlines = [DetallePrestamoInline]


@admin.register(DetallePrestamo)
class DetallePrestamoAdmin(admin.ModelAdmin):
    list_display = ("id", "prestamo", "nombre_equipo", "cantidad")
    search_fields = ("nombre_equipo", "prestamo__codigo")


@admin.register(PerfilSolicitante)
class PerfilSolicitanteAdmin(admin.ModelAdmin):
    list_display = ("solicitante", "documento_identidad", "telefono", "area_o_ciclo")


@admin.register(AutorizacionEspacio)
class AutorizacionEspacioAdmin(admin.ModelAdmin):
    list_display = ("solicitante", "espacio", "fecha_inicio", "fecha_fin", "estado")
    list_filter = ("estado",)
