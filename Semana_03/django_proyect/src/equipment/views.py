from django.shortcuts import render, redirect
from .models import Equipo
from .forms import EquipoForm


def equipo_list(request):
    equipos = Equipo.objects.all().order_by("id")
    return render(request, "equipment/equipo_list.html", {"equipos": equipos})


def equipo_create(request):
    if request.method == "POST":
        form = EquipoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("equipo_list")
    else:
        form = EquipoForm()

    return render(request, "equipment/equipo_form.html", {"form": form})
