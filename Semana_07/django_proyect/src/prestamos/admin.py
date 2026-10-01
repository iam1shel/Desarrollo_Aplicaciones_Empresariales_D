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

# Textos del panel /admin/ (Laboratorio 05). No cambia los modelos.
admin.site.site_header = "Préstamo de equipos — Administración"
admin.site.site_title = "Admin préstamos"
admin.site.index_title = "Laboratorio 05 · Django Admin"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "edificio", "piso", "aforo", "cupos_disponibles")
    search_fields = ("nombre", "edificio")


# OneToOneField: el perfil se edita en bloques, dentro del solicitante.
class PerfilSolicitanteInline(admin.StackedInline):
    model = PerfilSolicitante
    extra = 0


# ManyToMany through: las autorizaciones se editan en tabla, desde el solicitante.
class AutorizacionEspacioInline(admin.TabularInline):
    model = AutorizacionEspacio
    extra = 0
    fk_name = "solicitante"


# Entidad principal de prestamos: desde aquí se administran 1:1 y N:M. # display es columnasS
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
    search_fields = ("solicitante__nombre", "documento_identidad")


@admin.register(AutorizacionEspacio)
class AutorizacionEspacioAdmin(admin.ModelAdmin):
    list_display = ("solicitante", "espacio", "fecha_inicio", "fecha_fin", "estado")
    list_filter = ("estado",)
