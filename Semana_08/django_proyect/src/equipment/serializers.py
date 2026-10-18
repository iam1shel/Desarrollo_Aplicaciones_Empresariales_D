from rest_framework import serializers

from .models import Accesorio, AsignacionAccesorio, Equipo, FichaTecnica, Mantenimiento


class AccesorioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accesorio
        fields = ["id", "nombre", "tipo", "existencias"]

    def validate_nombre(self, value):
        nombre = value.strip()
        if len(nombre) < 3:
            raise serializers.ValidationError(
                "El nombre del accesorio debe tener al menos 3 caracteres."
            )
        repetidos = Accesorio.objects.filter(nombre__iexact=nombre)
        if self.instance is not None:
            repetidos = repetidos.exclude(pk=self.instance.pk)
        if repetidos.exists():
            raise serializers.ValidationError(
                "Ya existe un accesorio con ese nombre; sus existencias se llevan en un solo registro."
            )
        return nombre


class FichaTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaTecnica
        fields = ["numero_serie", "fecha_adquisicion", "garantia_hasta", "especificaciones"]


class MantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantenimiento
        fields = ["id", "fecha", "tipo", "tecnico", "descripcion"]


class AsignacionAccesorioSerializer(serializers.ModelSerializer):
    accesorio = serializers.CharField(source="accesorio.nombre")

    class Meta:
        model = AsignacionAccesorio
        fields = ["id", "accesorio", "cantidad", "fecha_asignacion", "estado"]


class EquipoSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source="get_estado_display")
    ficha = FichaTecnicaSerializer(allow_null=True)
    mantenimientos = MantenimientoSerializer(many=True)
    asignaciones_accesorio = AsignacionAccesorioSerializer(many=True)

    class Meta:
        model = Equipo
        fields = [
            "id",
            "nombre",
            "tipo",
            "marca",
            "ubicacion",
            "estado",
            "estado_display",
            "prestado_a",
            "ficha",
            "mantenimientos",
            "asignaciones_accesorio",
        ]
