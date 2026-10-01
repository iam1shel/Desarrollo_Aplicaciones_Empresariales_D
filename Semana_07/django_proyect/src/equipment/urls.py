from django.urls import path
from . import views

urlpatterns = [
    path("", views.equipo_list, name="equipo_list"),
    path("nuevo/", views.equipo_create, name="equipo_create"),
    path("asignar/", views.asignar_accesorio, name="asignar_accesorio"),
    path("reporte/", views.equipo_reporte, name="equipo_reporte"),
    path("<int:pk>/", views.equipo_detail, name="equipo_detail"),
]
