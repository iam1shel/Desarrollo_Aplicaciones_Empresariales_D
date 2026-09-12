from django.shortcuts import get_object_or_404, redirect, render
from .forms import EquipoForm
from .models import Equipo


def equipo_list(request):
    equipos = Equipo.objects.select_related("ficha").order_by("id")
    return render(request, "equipment/equipo_list.html", {"equipos": equipos})


def equipo_detail(request, pk):
    equipo = get_object_or_404(
        Equipo.objects.select_related("ficha").prefetch_related(
            "mantenimientos",
            "asignaciones_accesorio__accesorio",
        ),
        pk=pk,
    )
    return render(request, "equipment/equipo_detail.html", {"equipo": equipo})


def equipo_create(request):
    if request.method == "POST":
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("equipo_list")
    else:
        form = EquipoForm()

    return render(request, "equipment/equipo_form.html", {"form": form})
