from django.shortcuts import render, redirect
from .models import Equipo, equipos
from .forms import EquipoForm

def equipo_list(request):
    return render(request, 'equipment/equipo_list.html', {'equipos': equipos})


def equipo_create(request):
    if request.method == "POST":
        form = EquipoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            nuevo_id = len(equipos) + 1
            equipos.append(
                Equipo(
                    nuevo_id,
                    datos["nombre"],
                    datos["tipo"],
                    datos["marca"],
                    datos["ubicacion"],
                    datos["estado"],
                    datos["descripcion"],
                    datos["prestado_a"],
                )
            )
            return redirect("equipo_list")
    else:
        form = EquipoForm()

    return render(request, "equipment/equipo_form.html", {"form": form})