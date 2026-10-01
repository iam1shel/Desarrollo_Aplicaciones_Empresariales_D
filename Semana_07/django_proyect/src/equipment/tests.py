from datetime import date

from django.test import TestCase
from django.urls import reverse

from .models import Accesorio, AsignacionAccesorio, Equipo, FichaTecnica, Mantenimiento


class EquipoPersistenciaTests(TestCase):
    def test_listado_muestra_equipos_sembrados(self):
        respuesta = self.client.get(reverse("equipo_list"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Laptop 01")
        self.assertContains(respuesta, "LAPTOP")
        self.assertGreaterEqual(Equipo.objects.count(), 5)

    def test_crear_equipo_queda_en_sqlite(self):
        respuesta = self.client.post(
            reverse("equipo_create"),
            {
                "nombre": "Proyector 03",
                "tipo": "Proyector",
                "marca": "HP",
                "ubicacion": "Aula 500",
                "estado": "disponible",
                "prestado_a": "",
                "descripcion": "Prueba persistente",
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Equipo.objects.filter(nombre="Proyector 03").exists())

    def test_detalle_muestra_relaciones(self):
        laptop = Equipo.objects.get(nombre="Laptop 01")
        respuesta = self.client.get(reverse("equipo_detail", args=[laptop.pk]))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "LN-2026-001")
        self.assertContains(respuesta, "10/03/2025")
        self.assertContains(respuesta, "Cargador Lenovo 65W")
        self.assertContains(respuesta, "DISPONIBLE")
        self.assertTrue(FichaTecnica.objects.filter(equipo=laptop).exists())
        self.assertGreaterEqual(Mantenimiento.objects.filter(equipo=laptop).count(), 1)
        self.assertTrue(AsignacionAccesorio.objects.filter(equipo=laptop).exists())


class EquipoLab07Tests(TestCase):
    def test_reporte_y_filtros_del_queryset(self):
        self.assertEqual(self.client.get(reverse("equipo_reporte")).status_code, 200)
        disponibles = self.client.get(reverse("equipo_list"), {"filtro": "disponibles"})
        self.assertContains(disponibles, "Laptop 01")
        self.assertNotContains(disponibles, "Proyector 01")
        con_ficha = Equipo.objects.disponibles().con_ficha()
        self.assertTrue(con_ficha.filter(nombre="Laptop 01").exists())

    def test_asignar_descuenta_existencias(self):
        equipo = Equipo.objects.get(nombre="Laptop 02")
        estado_antes = equipo.estado
        accesorio = Accesorio.objects.get(nombre="Cable HDMI 2 m")
        accesorio.existencias = 5
        accesorio.save(update_fields=["existencias"])
        antes = AsignacionAccesorio.objects.count()

        respuesta = self.client.post(
            reverse("asignar_accesorio"),
            {
                "equipo": equipo.pk,
                "accesorio": accesorio.pk,
                "cantidad": 2,
                "fecha_asignacion": "2026-09-30",
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        accesorio.refresh_from_db()
        equipo.refresh_from_db()
        self.assertEqual(accesorio.existencias, 3)
        self.assertEqual(equipo.estado, estado_antes)
        self.assertEqual(AsignacionAccesorio.objects.count(), antes + 1)

    def test_asignar_sin_existencias_hace_rollback(self):
        equipo = Equipo.objects.get(nombre="Laptop 02")
        accesorio = Accesorio.objects.get(nombre="Cable HDMI 2 m")
        accesorio.existencias = 1
        accesorio.save(update_fields=["existencias"])
        antes = AsignacionAccesorio.objects.count()

        respuesta = self.client.post(
            reverse("asignar_accesorio"),
            {
                "equipo": equipo.pk,
                "accesorio": accesorio.pk,
                "cantidad": 4,
                "fecha_asignacion": date.today().isoformat(),
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "No hay existencias suficientes")
        accesorio.refresh_from_db()
        self.assertEqual(accesorio.existencias, 1)
        self.assertEqual(AsignacionAccesorio.objects.count(), antes)
