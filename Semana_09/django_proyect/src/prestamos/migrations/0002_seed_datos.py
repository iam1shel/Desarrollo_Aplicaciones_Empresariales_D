from datetime import date

from django.db import migrations


def cargar_datos(apps, schema_editor):
    Categoria = apps.get_model("prestamos", "Categoria")
    Espacio = apps.get_model("prestamos", "Espacio")
    Solicitante = apps.get_model("prestamos", "Solicitante")
    Prestamo = apps.get_model("prestamos", "Prestamo")
    DetallePrestamo = apps.get_model("prestamos", "DetallePrestamo")

    Categoria.objects.get_or_create(
        nombre="Laptop",
        defaults={"descripcion": "Computadoras portátiles para clases y estudio"},
    )
    Categoria.objects.get_or_create(
        nombre="Proyector",
        defaults={"descripcion": "Equipos de proyección para aulas"},
    )
    Categoria.objects.get_or_create(
        nombre="Accesorio",
        defaults={"descripcion": "Mouse, cables y periféricos"},
    )

    Espacio.objects.get_or_create(
        nombre="Biblioteca",
        defaults={"edificio": "Central", "piso": "1", "aforo": 80},
    )
    Espacio.objects.get_or_create(
        nombre="Aula 201",
        defaults={"edificio": "Ingeniería", "piso": "2", "aforo": 40},
    )
    Espacio.objects.get_or_create(
        nombre="Laboratorio 3",
        defaults={"edificio": "Cómputo", "piso": "3", "aforo": 25},
    )

    Solicitante.objects.get_or_create(
        codigo="U20261234",
        defaults={
            "nombre": "Ana Torres",
            "rol": "estudiante",
            "correo": "ana.torres@universidad.edu",
        },
    )
    Solicitante.objects.get_or_create(
        codigo="D1022",
        defaults={
            "nombre": "Carlos Medina",
            "rol": "docente",
            "correo": "cmedina@universidad.edu",
        },
    )

    prestamo, _ = Prestamo.objects.get_or_create(
        codigo="PR-001",
        defaults={
            "nombre_solicitante": "Ana Torres",
            "fecha_prestamo": date(2026, 8, 28),
            "fecha_estimada_devolucion": date(2026, 9, 4),
            "estado": "activo",
            "observaciones": "Uso para exposición de curso",
        },
    )
    DetallePrestamo.objects.get_or_create(
        prestamo=prestamo,
        nombre_equipo="Laptop 01",
        defaults={"cantidad": 1, "observacion": "Con cargador"},
    )
    DetallePrestamo.objects.get_or_create(
        prestamo=prestamo,
        nombre_equipo="Proyector 01",
        defaults={"cantidad": 1, "observacion": ""},
    )


def borrar_datos(apps, schema_editor):
    Categoria = apps.get_model("prestamos", "Categoria")
    Espacio = apps.get_model("prestamos", "Espacio")
    Solicitante = apps.get_model("prestamos", "Solicitante")
    Prestamo = apps.get_model("prestamos", "Prestamo")
    Categoria.objects.filter(nombre__in=["Laptop", "Proyector", "Accesorio"]).delete()
    Espacio.objects.filter(nombre__in=["Biblioteca", "Aula 201", "Laboratorio 3"]).delete()
    Solicitante.objects.filter(codigo__in=["U20261234", "D1022"]).delete()
    Prestamo.objects.filter(codigo="PR-001").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("prestamos", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(cargar_datos, borrar_datos),
    ]
