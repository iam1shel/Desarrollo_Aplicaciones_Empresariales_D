from django import forms
from .models import Categoria, Espacio, Solicitante, Prestamo, DetallePrestamo


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ["nombre", "descripcion"]
        widgets = {"descripcion": forms.Textarea(attrs={"rows": 3})}


class EspacioForm(forms.ModelForm):
    class Meta:
        model = Espacio
        fields = ["nombre", "edificio", "piso", "aforo"]


class SolicitanteForm(forms.ModelForm):
    class Meta:
        model = Solicitante
        fields = ["nombre", "codigo", "rol", "correo"]


class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            "codigo",
            "nombre_solicitante",
            "fecha_prestamo",
            "fecha_estimada_devolucion",
            "estado",
            "observaciones",
        ]
        widgets = {
            "fecha_prestamo": forms.DateInput(attrs={"type": "date"}, format="%Y-%m-%d"),
            "fecha_estimada_devolucion": forms.DateInput(
                attrs={"type": "date"}, format="%Y-%m-%d"
            ),
            "observaciones": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["fecha_prestamo"].input_formats = ["%Y-%m-%d"]
        self.fields["fecha_estimada_devolucion"].input_formats = ["%Y-%m-%d"]


class DetallePrestamoForm(forms.ModelForm):
    class Meta:
        model = DetallePrestamo
        fields = ["prestamo", "nombre_equipo", "cantidad", "observacion"]
