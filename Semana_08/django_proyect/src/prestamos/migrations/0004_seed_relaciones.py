from datetime import date

from django.db import migrations


def cargar(apps, schema_editor):
    Solicitante = apps.get_model("prestamos", "Solicitante")
    Espacio = apps.get_model("prestamos", "Espacio")
    PerfilSolicitante = apps.get_model("prestamos", "PerfilSolicitante")
    AutorizacionEspacio = apps.get_model("prestamos", "AutorizacionEspacio")

    ana = Solicitante.objects.filter(codigo="U20261234").first()
    carlos = Solicitante.objects.filter(codigo="D1022").first()
    biblioteca = Espacio.objects.filter(nombre="Biblioteca").first()
    aula = Espacio.objects.filter(nombre="Aula 201").first()
    lab = Espacio.objects.filter(nombre="Laboratorio 3").first()
    if not all([ana, carlos, biblioteca, aula, lab]):
        return

    PerfilSolicitante.objects.get_or_create(
        solicitante=ana,
        defaults={
            "documento_identidad": "71234567",
            "telefono": "987654321",
            "area_o_ciclo": "Ciclo V — Computación",
            "observaciones": "Puede retirar laptops en biblioteca",
        },
    )
    PerfilSolicitante.objects.get_or_create(
        solicitante=carlos,
        defaults={
            "documento_identidad": "40111222",
            "telefono": "999111222",
            "area_o_ciclo": "Docente de Ingeniería",
            "observaciones": "",
        },
    )

    AutorizacionEspacio.objects.get_or_create(
        solicitante=ana,
        espacio=biblioteca,
        defaults={
            "fecha_inicio": date(2026, 3, 1),
            "fecha_fin": date(2026, 12, 15),
            "estado": "vigente",
        },
    )
    AutorizacionEspacio.objects.get_or_create(
        solicitante=ana,
        espacio=lab,
        defaults={
            "fecha_inicio": date(2026, 8, 1),
            "fecha_fin": date(2026, 12, 15),
            "estado": "vigente",
        },
    )
    AutorizacionEspacio.objects.get_or_create(
        solicitante=carlos,
        espacio=aula,
        defaults={
            "fecha_inicio": date(2026, 3, 1),
            "fecha_fin": date(2026, 7, 31),
            "estado": "vencida",
        },
    )


def borrar(apps, schema_editor):
    PerfilSolicitante = apps.get_model("prestamos", "PerfilSolicitante")
    AutorizacionEspacio = apps.get_model("prestamos", "AutorizacionEspacio")
    PerfilSolicitante.objects.all().delete()
    AutorizacionEspacio.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("prestamos", "0003_autorizacionespacio_solicitante_espacios_and_more"),
    ]

    operations = [
        migrations.RunPython(cargar, borrar),
    ]
