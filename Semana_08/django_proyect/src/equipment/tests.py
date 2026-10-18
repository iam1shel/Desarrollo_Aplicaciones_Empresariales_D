from datetime import date

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Accesorio, AsignacionAccesorio, Equipo, FichaTecnica, Mantenimiento
from .serializers import AccesorioSerializer


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


class AccesorioSerializerLab08Tests(TestCase):
    def test_validate_nombre(self):
        valido = AccesorioSerializer(data={"nombre": "  Mouse inalámbrico ", "tipo": "Periférico", "existencias": 3})
        self.assertTrue(valido.is_valid(), valido.errors)
        self.assertEqual(valido.validated_data["nombre"], "Mouse inalámbrico")

        corto = AccesorioSerializer(data={"nombre": "ab", "tipo": "Video", "existencias": 1})
        self.assertFalse(corto.is_valid())
        self.assertIn("nombre", corto.errors)

        repetido = AccesorioSerializer(data={"nombre": "cable hdmi 2 m", "tipo": "Video", "existencias": 1})
        self.assertFalse(repetido.is_valid())
        self.assertIn("nombre", repetido.errors)


class AccesorioApiLab08Tests(APITestCase):
    def test_crud_y_codigos_de_estado(self):
        lista = self.client.get("/api/accesorios/")
        self.assertEqual(lista.status_code, status.HTTP_200_OK)

        cable = Accesorio.objects.get(nombre="Cable HDMI 2 m")
        detalle = self.client.get(f"/api/accesorios/{cable.pk}/")
        self.assertEqual(detalle.status_code, status.HTTP_200_OK)
        self.assertEqual(detalle.data["nombre"], "Cable HDMI 2 m")

        creado = self.client.post(
            "/api/accesorios/",
            {"nombre": "Puntero láser", "tipo": "Presentación", "existencias": 2},
            format="json",
        )
        self.assertEqual(creado.status_code, status.HTTP_201_CREATED)

        invalido = self.client.post(
            "/api/accesorios/",
            {"nombre": "ab", "tipo": "Video", "existencias": -1},
            format="json",
        )
        self.assertEqual(invalido.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("nombre", invalido.data)
        self.assertIn("existencias", invalido.data)

        pk = creado.data["id"]
        parcial = self.client.patch(f"/api/accesorios/{pk}/", {"existencias": 5}, format="json")
        self.assertEqual(parcial.status_code, status.HTTP_200_OK)
        self.assertEqual(parcial.data["existencias"], 5)

        borrado = self.client.delete(f"/api/accesorios/{pk}/")
        self.assertEqual(borrado.status_code, status.HTTP_204_NO_CONTENT)

        inexistente = self.client.get("/api/accesorios/99999/")
        self.assertEqual(inexistente.status_code, status.HTTP_404_NOT_FOUND)

    def test_vistas_genericas(self):
        self.assertEqual(self.client.get("/api/genericas/accesorios/").status_code, 200)
        cable = Accesorio.objects.get(nombre="Cable HDMI 2 m")
        self.assertEqual(self.client.get(f"/api/genericas/accesorios/{cable.pk}/").status_code, 200)

    def test_busqueda_y_ordenamiento(self):
        busqueda = self.client.get("/api/accesorios/", {"search": "hdmi"})
        self.assertEqual([a["nombre"] for a in busqueda.data], ["Cable HDMI 2 m"])

        Accesorio.objects.filter(nombre="Cable HDMI 2 m").update(existencias=7)
        orden = self.client.get("/api/accesorios/", {"ordering": "-existencias"})
        self.assertEqual(orden.data[0]["nombre"], "Cable HDMI 2 m")


class EquipoApiLab08Tests(APITestCase):
    def test_solo_lectura_con_relaciones_anidadas(self):
        laptop = Equipo.objects.get(nombre="Laptop 01")
        respuesta = self.client.get(f"/api/equipos/{laptop.pk}/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.data["ficha"]["numero_serie"], "LN-2026-001")
        self.assertTrue(respuesta.data["mantenimientos"])
        self.assertTrue(respuesta.data["asignaciones_accesorio"])

        self.assertEqual(self.client.post("/api/equipos/", {}, format="json").status_code, 405)

    def test_listado_optimizado(self):
        with self.assertNumQueries(4):
            self.client.get("/api/equipos/")

    def test_filtro_estado_y_accion_disponibles(self):
        prestados = self.client.get("/api/equipos/", {"estado": "prestado"})
        self.assertTrue(prestados.data)
        self.assertTrue(all(e["estado"] == "prestado" for e in prestados.data))

        disponibles = self.client.get("/api/equipos/disponibles/")
        self.assertEqual(
            {e["nombre"] for e in disponibles.data},
            set(Equipo.objects.disponibles().values_list("nombre", flat=True)),
        )

        con_ficha = self.client.get("/api/equipos/disponibles/", {"con_ficha": "1"})
        self.assertEqual(
            {e["nombre"] for e in con_ficha.data},
            set(Equipo.objects.disponibles().con_ficha().values_list("nombre", flat=True)),
        )
