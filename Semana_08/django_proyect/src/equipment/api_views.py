from rest_framework import filters, generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Accesorio, Equipo
from .serializers import AccesorioSerializer, EquipoSerializer


# Ejercicio 4: primera versión con vistas genéricas. Se conservan en /api/genericas/
# para comparar con el ViewSet que las reemplaza en /api/accesorios/.
class AccesorioListCreateAPIView(generics.ListCreateAPIView):
    queryset = Accesorio.objects.all()
    serializer_class = AccesorioSerializer


class AccesorioRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accesorio.objects.all()
    serializer_class = AccesorioSerializer


class AccesorioViewSet(viewsets.ModelViewSet):
    queryset = Accesorio.objects.all()
    serializer_class = AccesorioSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["nombre", "tipo"]
    ordering_fields = ["nombre", "tipo", "existencias"]
    ordering = ["nombre"]


class EquipoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = EquipoSerializer

    def get_queryset(self):
        equipos = Equipo.objects.select_related("ficha").prefetch_related(
            "mantenimientos",
            "asignaciones_accesorio__accesorio",
        )
        estado = self.request.query_params.get("estado")
        if estado:
            equipos = equipos.filter(estado=estado)
        return equipos

    @action(detail=False)
    def disponibles(self, request):
        equipos = self.get_queryset().disponibles()
        if request.query_params.get("con_ficha") == "1":
            equipos = equipos.con_ficha()
        serializer = self.get_serializer(equipos, many=True)
        return Response(serializer.data)
