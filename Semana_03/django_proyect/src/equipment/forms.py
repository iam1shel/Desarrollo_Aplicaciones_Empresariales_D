from django import forms
from .models import Equipo


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
