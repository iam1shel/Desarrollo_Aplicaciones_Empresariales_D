from django.shortcuts import get_object_or_404, redirect, render
from .forms import (
    CategoriaForm,
    DetallePrestamoForm,
    EspacioForm,
    PrestamoForm,
    SolicitanteForm,
)
from .models import Categoria, DetallePrestamo, Espacio, Prestamo, Solicitante


def prestamos_home(request):
    return render(
        request,
        "prestamos/home.html",
        {
            "total_categorias": Categoria.objects.count(),
            "total_espacios": Espacio.objects.count(),
            "total_solicitantes": Solicitante.objects.count(),
            "total_prestamos": Prestamo.objects.count(),
            "prestamos_activos": Prestamo.objects.filter(estado="activo").count(),
            "total_detalles": DetallePrestamo.objects.count(),
        },
    )


def categoria_list(request):
    categorias = Categoria.objects.all().order_by("nombre")
    return render(request, "prestamos/categoria_list.html", {"categorias": categorias})


def categoria_create(request):
    form = CategoriaForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("categoria_list")
    return render(
        request,
        "prestamos/form.html",
        {"form": form, "titulo": "Registrar categoría", "url_cancelar": "categoria_list"},
    )


def categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("categoria_list")
    return render(
        request,
        "prestamos/form.html",
        {"form": form, "titulo": "Editar categoría", "url_cancelar": "categoria_list"},
    )


def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == "POST":
        categoria.delete()
        return redirect("categoria_list")
    return render(
        request,
        "prestamos/confirm_delete.html",
        {
            "objeto": categoria,
            "tipo": "categoría",
            "url_cancelar": "categoria_list",
        },
    )


def espacio_list(request):
    espacios = Espacio.objects.all().order_by("edificio", "nombre")
    return render(request, "prestamos/espacio_list.html", {"espacios": espacios})


def espacio_create(request):
    form = EspacioForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("espacio_list")
    return render(
        request,
        "prestamos/form.html",
        {"form": form, "titulo": "Registrar espacio", "url_cancelar": "espacio_list"},
    )


def espacio_update(request, pk):
    espacio = get_object_or_404(Espacio, pk=pk)
    form = EspacioForm(request.POST or None, instance=espacio)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("espacio_list")
    return render(
        request,
        "prestamos/form.html",
        {"form": form, "titulo": "Editar espacio", "url_cancelar": "espacio_list"},
    )


def espacio_delete(request, pk):
    espacio = get_object_or_404(Espacio, pk=pk)
    if request.method == "POST":
        espacio.delete()
        return redirect("espacio_list")
    return render(
        request,
        "prestamos/confirm_delete.html",
        {"objeto": espacio, "tipo": "espacio", "url_cancelar": "espacio_list"},
    )


def solicitante_list(request):
    rol = request.GET.get("rol")
    solicitantes = Solicitante.objects.all()
    if rol:
        solicitantes = solicitantes.filter(rol=rol)
    solicitantes = solicitantes.order_by("nombre")
    return render(
        request,
        "prestamos/solicitante_list.html",
        {"solicitantes": solicitantes, "rol": rol},
    )


def solicitante_create(request):
    form = SolicitanteForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("solicitante_list")
    return render(
        request,
        "prestamos/form.html",
        {"form": form, "titulo": "Registrar solicitante", "url_cancelar": "solicitante_list"},
    )


def solicitante_update(request, pk):
    solicitante = get_object_or_404(Solicitante, pk=pk)
    form = SolicitanteForm(request.POST or None, instance=solicitante)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("solicitante_list")
    return render(
        request,
        "prestamos/form.html",
        {"form": form, "titulo": "Editar solicitante", "url_cancelar": "solicitante_list"},
    )


def solicitante_delete(request, pk):
    solicitante = get_object_or_404(Solicitante, pk=pk)
    if request.method == "POST":
        solicitante.delete()
        return redirect("solicitante_list")
    return render(
        request,
        "prestamos/confirm_delete.html",
        {"objeto": solicitante, "tipo": "solicitante", "url_cancelar": "solicitante_list"},
    )


def prestamo_list(request):
    estado = request.GET.get("estado")
    prestamos = Prestamo.objects.all().prefetch_related("detalles")
    if estado:
        prestamos = prestamos.filter(estado=estado)
    prestamos = prestamos.order_by("-fecha_prestamo")
    return render(
        request,
        "prestamos/prestamo_list.html",
        {"prestamos": prestamos, "estado": estado},
    )


def prestamo_create(request):
    form = PrestamoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("prestamo_list")
    return render(
        request,
        "prestamos/form.html",
        {"form": form, "titulo": "Registrar préstamo", "url_cancelar": "prestamo_list"},
    )


def prestamo_update(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    form = PrestamoForm(request.POST or None, instance=prestamo)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("prestamo_list")
    return render(
        request,
        "prestamos/form.html",
        {"form": form, "titulo": "Editar préstamo", "url_cancelar": "prestamo_list"},
    )


def prestamo_delete(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if request.method == "POST":
        prestamo.delete()
        return redirect("prestamo_list")
    return render(
        request,
        "prestamos/confirm_delete.html",
        {"objeto": prestamo, "tipo": "préstamo", "url_cancelar": "prestamo_list"},
    )


def detalle_list(request):
    detalles = DetallePrestamo.objects.select_related("prestamo").order_by("id")
    return render(request, "prestamos/detalle_list.html", {"detalles": detalles})


def detalle_create(request):
    form = DetallePrestamoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("detalle_list")
    return render(
        request,
        "prestamos/form.html",
        {"form": form, "titulo": "Registrar detalle de préstamo", "url_cancelar": "detalle_list"},
    )


def detalle_update(request, pk):
    detalle = get_object_or_404(DetallePrestamo, pk=pk)
    form = DetallePrestamoForm(request.POST or None, instance=detalle)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("detalle_list")
    return render(
        request,
        "prestamos/form.html",
        {"form": form, "titulo": "Editar detalle de préstamo", "url_cancelar": "detalle_list"},
    )


def detalle_delete(request, pk):
    detalle = get_object_or_404(DetallePrestamo, pk=pk)
    if request.method == "POST":
        detalle.delete()
        return redirect("detalle_list")
    return render(
        request,
        "prestamos/confirm_delete.html",
        {"objeto": detalle, "tipo": "detalle de préstamo", "url_cancelar": "detalle_list"},
    )
