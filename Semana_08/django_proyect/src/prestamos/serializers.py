from rest_framework import serializers

from .models import (
    AutorizacionEspacio,
    Categoria,
    DetallePrestamo,
    Espacio,
    PerfilSolicitante,
    Prestamo,
    Solicitante,
)


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nombre", "descripcion"]


class EspacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Espacio
        fields = ["id", "nombre", "edificio", "piso", "aforo", "cupos_disponibles"]

    def validate_aforo(self, value):
        if value < 1:
            raise serializers.ValidationError(
                "El aforo debe ser de al menos una persona."
            )
        return value


class PerfilSolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilSolicitante
        fields = ["documento_identidad", "telefono", "area_o_ciclo"]


class AutorizacionEspacioSerializer(serializers.ModelSerializer):
    espacio = serializers.CharField(source="espacio.nombre")
    edificio = serializers.CharField(source="espacio.edificio")

    class Meta:
        model = AutorizacionEspacio
        fields = ["id", "espacio", "edificio", "fecha_inicio", "fecha_fin", "estado"]


class SolicitanteSerializer(serializers.ModelSerializer):
    rol_display = serializers.CharField(source="get_rol_display")
    perfil = PerfilSolicitanteSerializer(allow_null=True)
    autorizaciones = AutorizacionEspacioSerializer(many=True)

    class Meta:
        model = Solicitante
        fields = [
            "id",
            "nombre",
            "codigo",
            "rol",
            "rol_display",
            "correo",
            "perfil",
            "autorizaciones",
        ]


class DetallePrestamoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePrestamo
        fields = ["id", "nombre_equipo", "cantidad", "observacion"]


class PrestamoSerializer(serializers.ModelSerializer):
    estado_display = serializers.CharField(source="get_estado_display")
    detalles = DetallePrestamoSerializer(many=True)

    class Meta:
        model = Prestamo
        fields = [
            "id",
            "codigo",
            "nombre_solicitante",
            "fecha_prestamo",
            "fecha_estimada_devolucion",
            "estado",
            "estado_display",
            "observaciones",
            "detalles",
        ]
