from datetime import date

from django.db import migrations


def cargar(apps, schema_editor):
    Equipo = apps.get_model("equipment", "Equipo")
    FichaTecnica = apps.get_model("equipment", "FichaTecnica")
    Mantenimiento = apps.get_model("equipment", "Mantenimiento")
    Accesorio = apps.get_model("equipment", "Accesorio")
    AsignacionAccesorio = apps.get_model("equipment", "AsignacionAccesorio")

    laptop = Equipo.objects.filter(nombre="Laptop 01").first()
    proyector = Equipo.objects.filter(nombre="Proyector 01").first()
    if not laptop or not proyector:
        return

    FichaTecnica.objects.get_or_create(
        equipo=laptop,
        defaults={
            "numero_serie": "LN-2026-001",
            "fecha_adquisicion": date(2025, 3, 10),
            "garantia_hasta": date(2027, 3, 10),
            "especificaciones": "16 GB RAM, SSD 512 GB",
        },
    )
    FichaTecnica.objects.get_or_create(
        equipo=proyector,
        defaults={
            "numero_serie": "EP-201-088",
            "fecha_adquisicion": date(2024, 8, 1),
            "garantia_hasta": date(2026, 8, 1),
            "especificaciones": "3800 lúmenes, HDMI",
        },
    )

    Mantenimiento.objects.get_or_create(
        equipo=laptop,
        fecha=date(2026, 7, 15),
        defaults={
            "tipo": "preventivo",
            "tecnico": "Luis Paredes",
            "descripcion": "Limpieza de ventiladores y actualización de BIOS",
        },
    )
    Mantenimiento.objects.get_or_create(
        equipo=laptop,
        fecha=date(2026, 8, 20),
        defaults={
            "tipo": "correctivo",
            "tecnico": "María Quispe",
            "descripcion": "Cambio de teclado",
        },
    )

    cargador, _ = Accesorio.objects.get_or_create(
        nombre="Cargador Lenovo 65W",
        defaults={"tipo": "Energía"},
    )
    hdmi, _ = Accesorio.objects.get_or_create(
        nombre="Cable HDMI 2 m",
        defaults={"tipo": "Video"},
    )

    AsignacionAccesorio.objects.get_or_create(
        equipo=laptop,
        accesorio=cargador,
        defaults={
            "cantidad": 1,
            "fecha_asignacion": date(2026, 3, 12),
            "estado": "vigente",
        },
    )
    AsignacionAccesorio.objects.get_or_create(
        equipo=proyector,
        accesorio=hdmi,
        defaults={
            "cantidad": 1,
            "fecha_asignacion": date(2026, 8, 1),
            "estado": "vigente",
        },
    )


def borrar(apps, schema_editor):
    Accesorio = apps.get_model("equipment", "Accesorio")
    Accesorio.objects.filter(
        nombre__in=["Cargador Lenovo 65W", "Cable HDMI 2 m"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("equipment", "0003_accesorio_asignacionaccesorio_accesorio_equipos_and_more"),
    ]

    operations = [
        migrations.RunPython(cargar, borrar),
    ]
