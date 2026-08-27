from django import forms


class EquipoForm(forms.Form):
    nombre = forms.CharField(label="Nombre", max_length=100)
    tipo = forms.CharField(label="Tipo", max_length=50)
    marca = forms.CharField(label="Marca", max_length=50)
    ubicacion = forms.CharField(label="Ubicación", max_length=100)
    estado = forms.ChoiceField(
        label="Estado",
        choices=[
            ("disponible", "Disponible"),
            ("prestado", "Prestado"),
        ],
    )
    prestado_a = forms.CharField(
        label="¿Quién lo tiene?",
        max_length=100,
        required=False,
    )
    descripcion = forms.CharField(
        label="Descripción",
        required=False,
        widget=forms.Textarea,
    )