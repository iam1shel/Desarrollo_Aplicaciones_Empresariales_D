from datetime import date

from django import forms
from django.core.validators import MinValueValidator

from .models import AsignacionAccesorio, Equipo


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = [
            "nombre",
            "tipo",
            "marca",
            "ubicacion",
            "estado",
            "prestado_a",
            "descripcion",
        ]
        labels = {
            "nombre": "Nombre",
            "tipo": "Tipo",
            "marca": "Marca",
            "ubicacion": "Ubicación",
            "estado": "Estado",
            "prestado_a": "¿Quién lo tiene?",
            "descripcion": "Descripción",
        }
        widgets = {
            "descripcion": forms.Textarea(attrs={"rows": 3}),
        }


class AsignarAccesorioForm(forms.ModelForm):
    cantidad = forms.IntegerField(
        min_value=1,
        initial=1,
        validators=[MinValueValidator(1)],
        label="Cantidad",
    )

    class Meta:
        model = AsignacionAccesorio
        fields = ["equipo", "accesorio", "cantidad", "fecha_asignacion"]
        widgets = {
            "fecha_asignacion": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha_asignacion"].input_formats = ["%Y-%m-%d"]
        self.fields["fecha_asignacion"].initial = date.today()
