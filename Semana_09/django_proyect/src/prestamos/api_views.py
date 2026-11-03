from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Categoria, Espacio, Prestamo, Solicitante
from .serializers import (
    CategoriaSerializer,
    EspacioSerializer,
    PrestamoSerializer,
    SolicitanteSerializer,
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class EspacioViewSet(viewsets.ModelViewSet):
    queryset = Espacio.objects.all()
    serializer_class = EspacioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "edificio"]
    ordering_fields = ["nombre", "aforo", "cupos_disponibles"]
    ordering = ["nombre"]


class SolicitanteViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SolicitanteSerializer

    def get_queryset(self):
        solicitantes = Solicitante.objects.select_related("perfil").prefetch_related(
            "autorizaciones__espacio"
        )
        rol = self.request.query_params.get("rol")
        if rol:
            solicitantes = solicitantes.filter(rol=rol)
        return solicitantes


class PrestamoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PrestamoSerializer

    def get_queryset(self):
        prestamos = Prestamo.objects.prefetch_related("detalles")
        estado = self.request.query_params.get("estado")
        if estado:
            prestamos = prestamos.filter(estado=estado)
        return prestamos

    @action(detail=False)
    def activos(self, request):
        serializer = self.get_serializer(self.get_queryset().activos(), many=True)
        return Response(serializer.data)

    @action(detail=False, url_path="del-mes")
    def del_mes(self, request):
        serializer = self.get_serializer(self.get_queryset().del_mes(), many=True)
        return Response(serializer.data)
