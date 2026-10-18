from django.urls import include, path
from rest_framework.routers import DefaultRouter

from equipment import api_views as equipment_api
from prestamos import api_views as prestamos_api

router = DefaultRouter()
router.register("accesorios", equipment_api.AccesorioViewSet, basename="accesorio")
router.register("equipos", equipment_api.EquipoViewSet, basename="equipo")
router.register("categorias", prestamos_api.CategoriaViewSet, basename="categoria")
router.register("espacios", prestamos_api.EspacioViewSet, basename="espacio")
router.register("solicitantes", prestamos_api.SolicitanteViewSet, basename="solicitante")
router.register("prestamos", prestamos_api.PrestamoViewSet, basename="prestamo")

urlpatterns = [
    path(
        "genericas/accesorios/",
        equipment_api.AccesorioListCreateAPIView.as_view(),
        name="accesorio-generica-list",
    ),
    path(
        "genericas/accesorios/<int:pk>/",
        equipment_api.AccesorioRetrieveUpdateDestroyAPIView.as_view(),
        name="accesorio-generica-detail",
    ),
    path("", include(router.urls)),
]
