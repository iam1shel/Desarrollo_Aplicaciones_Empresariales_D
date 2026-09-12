from django.db import migrations


EQUIPOS = [
    ("Laptop 01", "Laptop", "Lenovo", "Biblioteca", "disponible", "Uso en sala de estudio", ""),
    ("Proyector 01", "Proyector", "Epson", "Aula 201", "prestado", "", ""),
    ("Mouse 01", "Mouse", "Acer", "Aula 1501", "prestado", "", ""),
    ("Laptop 02", "Laptop", "HP", "Biblioteca", "disponible", "Uso en sala de estudio", ""),
    ("Tablet 01", "Tablet", "Honor", "Aula 505", "prestado", "", ""),
]


def cargar_equipos(apps, schema_editor):
    Equipo = apps.get_model("equipment", "Equipo")
    for nombre, tipo, marca, ubicacion, estado, descripcion, prestado_a in EQUIPOS:
        Equipo.objects.get_or_create(
            nombre=nombre,
            defaults={
                "tipo": tipo,
                "marca": marca,
                "ubicacion": ubicacion,
                "estado": estado,
                "descripcion": descripcion,
                "prestado_a": prestado_a,
            },
        )


def borrar_equipos(apps, schema_editor):
    Equipo = apps.get_model("equipment", "Equipo")
    Equipo.objects.filter(nombre__in=[fila[0] for fila in EQUIPOS]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("equipment", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(cargar_equipos, borrar_equipos),
    ]
