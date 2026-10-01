from django.db import transaction
from django.db.models import Count, F, Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import AsignarAccesorioForm, EquipoForm
from .models import Accesorio, AsignacionAccesorio, Equipo


class ExistenciaInsuficiente(Exception):
    pass


def equipo_list(request):
    equipos = Equipo.objects.select_related("ficha").order_by("id")
    filtro = request.GET.get("filtro", "")
    if filtro == "disponibles":
        equipos = equipos.disponibles()
    elif filtro == "con_ficha":
        equipos = equipos.con_ficha()
    elif filtro == "disponibles_con_ficha":
        equipos = equipos.disponibles().con_ficha()
    return render(
        request,
        "equipment/equipo_list.html",
        {"equipos": equipos, "filtro": filtro},
    )


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


def asignar_accesorio(request):
    form = AsignarAccesorioForm(request.POST or None)
    error = None
    if request.method == "POST" and form.is_valid():
        try:
            with transaction.atomic():
                asignacion = form.save(commit=False)
                asignacion.estado = "vigente"
                asignacion.save()
                accesorio = Accesorio.objects.select_for_update().get(
                    pk=asignacion.accesorio_id
                )
                if accesorio.existencias < asignacion.cantidad:
                    raise ExistenciaInsuficiente(
                        "No hay existencias suficientes para esta asignación. "
                        "La operación se canceló y no se guardó ningún cambio."
                    )
                Accesorio.objects.filter(pk=accesorio.pk).update(
                    existencias=F("existencias") - asignacion.cantidad
                )
        except ExistenciaInsuficiente as exc:
            error = str(exc)
        else:
            return redirect("equipo_detail", pk=asignacion.equipo_id)

    return render(
        request,
        "equipment/asignar_accesorio.html",
        {"form": form, "error": error},
    )


def equipo_reporte(request):
    totales = AsignacionAccesorio.objects.aggregate(total_unidades=Sum("cantidad"))
    equipos = Equipo.objects.annotate(
        num_mantenimientos=Count("mantenimientos")
    ).order_by("-num_mantenimientos", "nombre")
    por_estado = AsignacionAccesorio.objects.values("estado").annotate(
        asignaciones=Count("id"),
        unidades=Sum("cantidad"),
    ).order_by("-unidades", "-asignaciones")
    etiquetas = dict(AsignacionAccesorio.ESTADOS)
    for fila in por_estado:
        fila["estado_label"] = etiquetas.get(fila["estado"], fila["estado"])
    disponibles_con_ficha = Equipo.objects.disponibles().con_ficha().order_by("nombre")
    return render(
        request,
        "equipment/reporte.html",
        {
            "total_unidades": totales["total_unidades"] or 0,
            "equipos": equipos,
            "por_estado": por_estado,
            "disponibles_con_ficha": disponibles_con_ficha,
        },
    )
