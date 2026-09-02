from django.urls import path
from . import views

urlpatterns = [
    path("", views.prestamos_home, name="prestamos_home"),
    path("categorias/", views.categoria_list, name="categoria_list"),
    path("categorias/nuevo/", views.categoria_create, name="categoria_create"),
    path("categorias/<int:pk>/editar/", views.categoria_update, name="categoria_update"),
    path("categorias/<int:pk>/eliminar/", views.categoria_delete, name="categoria_delete"),
    path("espacios/", views.espacio_list, name="espacio_list"),
    path("espacios/nuevo/", views.espacio_create, name="espacio_create"),
    path("espacios/<int:pk>/editar/", views.espacio_update, name="espacio_update"),
    path("espacios/<int:pk>/eliminar/", views.espacio_delete, name="espacio_delete"),
    path("solicitantes/", views.solicitante_list, name="solicitante_list"),
    path("solicitantes/nuevo/", views.solicitante_create, name="solicitante_create"),
    path("solicitantes/<int:pk>/editar/", views.solicitante_update, name="solicitante_update"),
    path("solicitantes/<int:pk>/eliminar/", views.solicitante_delete, name="solicitante_delete"),
    path("registros/", views.prestamo_list, name="prestamo_list"),
    path("registros/nuevo/", views.prestamo_create, name="prestamo_create"),
    path("registros/<int:pk>/editar/", views.prestamo_update, name="prestamo_update"),
    path("registros/<int:pk>/eliminar/", views.prestamo_delete, name="prestamo_delete"),
    path("detalles/", views.detalle_list, name="detalle_list"),
    path("detalles/nuevo/", views.detalle_create, name="detalle_create"),
    path("detalles/<int:pk>/editar/", views.detalle_update, name="detalle_update"),
    path("detalles/<int:pk>/eliminar/", views.detalle_delete, name="detalle_delete"),
]
