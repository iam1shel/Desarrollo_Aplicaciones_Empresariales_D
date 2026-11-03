from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import AutorizacionEspacio, Categoria, DetallePrestamo, Espacio, Prestamo, Solicitante
from .serializers import EspacioSerializer


class PrestamosCrudTests(TestCase):
    def test_home_y_listados(self):
        for nombre in [
            "prestamos_home",
            "categoria_list",
            "espacio_list",
            "solicitante_list",
            "prestamo_list",
            "detalle_list",
            "autorizacion_list",
        ]:
            respuesta = self.client.get(reverse(nombre))
            self.assertEqual(respuesta.status_code, 200, nombre)

    def test_filtro_solicitantes_por_rol(self):
        respuesta = self.client.get(reverse("solicitante_list"), {"rol": "docente"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Carlos Medina")
        self.assertNotContains(respuesta, "Ana Torres")

    def test_filtro_prestamos_activos(self):
        respuesta = self.client.get(reverse("prestamo_list"), {"estado": "activo"})
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "PR-001")

    def test_crear_categoria(self):
        respuesta = self.client.post(
            reverse("categoria_create"),
            {"nombre": "Tablet", "descripcion": "Tablets institucionales"},
        )
        self.assertEqual(respuesta.status_code, 302)
        self.assertTrue(Categoria.objects.filter(nombre="Tablet").exists())

    def test_actualizar_prestamo(self):
        prestamo = Prestamo.objects.get(codigo="PR-001")
        respuesta = self.client.post(
            reverse("prestamo_update", args=[prestamo.pk]),
            {
                "codigo": "PR-001",
                "nombre_solicitante": "Ana Torres",
                "fecha_prestamo": "2026-08-28",
                "fecha_estimada_devolucion": "2026-09-04",
                "estado": "devuelto",
                "observaciones": "Devuelto en prueba",
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        prestamo.refresh_from_db()
        self.assertEqual(prestamo.estado, "devuelto")

    def test_eliminar_detalle_requiere_post(self):
        detalle = DetallePrestamo.objects.first()
        pk = detalle.pk
        get_resp = self.client.get(reverse("detalle_delete", args=[pk]))
        self.assertEqual(get_resp.status_code, 200)
        self.assertTrue(DetallePrestamo.objects.filter(pk=pk).exists())

        post_resp = self.client.post(reverse("detalle_delete", args=[pk]))
        self.assertEqual(post_resp.status_code, 302)
        self.assertFalse(DetallePrestamo.objects.filter(pk=pk).exists())

    def test_solicitante_muestra_perfil_y_autorizaciones(self):
        respuesta = self.client.get(reverse("solicitante_list"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "71234567")
        self.assertContains(respuesta, "Biblioteca")

    def test_crud_autorizacion_intermedia(self):
        self.assertEqual(self.client.get(reverse("autorizacion_list")).status_code, 200)
        solicitante = Solicitante.objects.get(codigo="D1022")
        lab = Espacio.objects.get(nombre="Laboratorio 3")
        crear = self.client.post(
            reverse("autorizacion_create"),
            {
                "solicitante": solicitante.pk,
                "espacio": lab.pk,
                "fecha_inicio": "2026-09-01",
                "fecha_fin": "2026-12-15",
                "estado": "vigente",
            },
        )
        self.assertEqual(crear.status_code, 302)
        aut = AutorizacionEspacio.objects.get(solicitante=solicitante, espacio=lab)
        editar = self.client.post(
            reverse("autorizacion_update", args=[aut.pk]),
            {
                "solicitante": solicitante.pk,
                "espacio": lab.pk,
                "fecha_inicio": "2026-09-01",
                "fecha_fin": "2026-12-15",
                "estado": "revocada",
            },
        )
        self.assertEqual(editar.status_code, 302)
        aut.refresh_from_db()
        self.assertEqual(aut.estado, "revocada")
        borrar = self.client.post(reverse("autorizacion_delete", args=[aut.pk]))
        self.assertEqual(borrar.status_code, 302)
        self.assertFalse(AutorizacionEspacio.objects.filter(pk=aut.pk).exists())

    def test_plantillas_filtran_fechas_y_escapan_html(self):
        listado = self.client.get(reverse("prestamo_list"))
        self.assertContains(listado, "28/08/2026")
        self.assertContains(listado, "04/09/2026")
        self.assertContains(listado, "Semana 08")

        Categoria.objects.create(
            nombre="XSS",
            descripcion="<script>alert(1)</script>",
        )
        categorias = self.client.get(reverse("categoria_list"))
        self.assertContains(categorias, "&lt;script&gt;alert(1)&lt;/script&gt;")
        self.assertNotContains(categorias, "<script>alert(1)</script>")

        solicitantes = self.client.get(reverse("solicitante_list"))
        self.assertContains(solicitantes, "Biblioteca")
        self.assertContains(solicitantes, "VIGENTE")


class AdminLab05Tests(TestCase):
    """Comprueba que las 7 entidades de prestamos están en Django Admin."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_superuser(
            "admin", "admin@localhost", "Prestamo2026!"
        )
        self.client.force_login(self.user)

    def test_siete_entidades_registradas(self):
        modelos = [
            "categoria",
            "espacio",
            "solicitante",
            "prestamo",
            "detalleprestamo",
            "perfilsolicitante",
            "autorizacionespacio",
        ]
        for modelo in modelos:
            url = f"/admin/prestamos/{modelo}/"
            respuesta = self.client.get(url)
            self.assertEqual(respuesta.status_code, 200, url)

    def test_solicitante_usa_inlines(self):
        solicitante = Solicitante.objects.first()
        url = reverse("admin:prestamos_solicitante_change", args=[solicitante.pk])
        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'id="perfil-group"')
        self.assertContains(respuesta, 'id="autorizaciones-group"')


class PrestamosLab07Tests(TestCase):
    def test_reporte_y_queryset_de_prestamos(self):
        inicio = self.client.get(reverse("prestamos_home"))
        self.assertEqual(inicio.status_code, 200)
        self.assertContains(inicio, "préstamo(s) activo(s)")
        activos = self.client.get(reverse("prestamo_list"), {"estado": "activo", "mes": "actual"})
        self.assertEqual(activos.status_code, 200)
        self.assertEqual(self.client.get(reverse("prestamo_reporte")).status_code, 200)
        self.assertEqual(
            Prestamo.objects.activos().count(),
            Prestamo.objects.filter(estado="activo").count(),
        )

    def test_autorizar_descuenta_un_cupo_sin_tocar_aforo(self):
        espacio = Espacio.objects.get(nombre="Biblioteca")
        espacio.cupos_disponibles = 2
        espacio.save(update_fields=["cupos_disponibles"])
        aforo = espacio.aforo
        solicitante = Solicitante.objects.get(codigo="D1022")
        antes = AutorizacionEspacio.objects.count()

        respuesta = self.client.post(
            reverse("autorizar_espacio"),
            {
                "solicitante": solicitante.pk,
                "espacio": espacio.pk,
                "fecha_inicio": "2026-09-01",
                "fecha_fin": "2026-12-15",
                "estado": "vigente",
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        espacio.refresh_from_db()
        self.assertEqual(espacio.cupos_disponibles, 1)
        self.assertEqual(espacio.aforo, aforo)
        self.assertEqual(AutorizacionEspacio.objects.count(), antes + 1)

    def test_autorizar_sin_cupo_hace_rollback(self):
        espacio = Espacio.objects.get(nombre="Aula 201")
        espacio.cupos_disponibles = 0
        espacio.save(update_fields=["cupos_disponibles"])
        solicitante = Solicitante.objects.get(codigo="U20261234")
        antes = AutorizacionEspacio.objects.count()

        respuesta = self.client.post(
            reverse("autorizar_espacio"),
            {
                "solicitante": solicitante.pk,
                "espacio": espacio.pk,
                "fecha_inicio": "2026-09-01",
                "fecha_fin": "2026-12-15",
                "estado": "vigente",
            },
        )
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "No hay cupos disponibles")
        espacio.refresh_from_db()
        self.assertEqual(espacio.cupos_disponibles, 0)
        self.assertEqual(AutorizacionEspacio.objects.count(), antes)


class EspacioSerializerLab08Tests(TestCase):
    def test_validate_aforo(self):
        valido = EspacioSerializer(data={"nombre": "Sala 105", "edificio": "Central", "aforo": 30})
        self.assertTrue(valido.is_valid(), valido.errors)

        invalido = EspacioSerializer(data={"nombre": "Depósito", "edificio": "Central", "aforo": 0})
        self.assertFalse(invalido.is_valid())
        self.assertIn("aforo", invalido.errors)


class PrestamosApiLab08Tests(APITestCase):
    def test_raiz_de_la_api(self):
        respuesta = self.client.get("/api/")
        self.assertEqual(respuesta.status_code, 200)
        for recurso in ["accesorios", "equipos", "categorias", "espacios", "solicitantes", "prestamos"]:
            self.assertIn(recurso, respuesta.data)

    def test_crud_espacios_y_codigos_de_estado(self):
        self.assertEqual(self.client.get("/api/espacios/").status_code, status.HTTP_200_OK)

        creado = self.client.post(
            "/api/espacios/",
            {"nombre": "Sala 105", "edificio": "Central", "piso": "1", "aforo": 30},
            format="json",
        )
        self.assertEqual(creado.status_code, status.HTTP_201_CREATED)

        invalido = self.client.post(
            "/api/espacios/",
            {"nombre": "Depósito", "edificio": "Central", "aforo": 0},
            format="json",
        )
        self.assertEqual(invalido.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("aforo", invalido.data)

        pk = creado.data["id"]
        self.assertEqual(self.client.get(f"/api/espacios/{pk}/").status_code, status.HTTP_200_OK)
        editado = self.client.put(
            f"/api/espacios/{pk}/",
            {"nombre": "Sala 105", "edificio": "Central", "piso": "1", "aforo": 35, "cupos_disponibles": 2},
            format="json",
        )
        self.assertEqual(editado.status_code, status.HTTP_200_OK)
        self.assertEqual(editado.data["aforo"], 35)

        self.assertEqual(self.client.delete(f"/api/espacios/{pk}/").status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.client.get(f"/api/espacios/{pk}/").status_code, status.HTTP_404_NOT_FOUND)

    def test_crud_categorias(self):
        creada = self.client.post("/api/categorias/", {"nombre": "Tablet"}, format="json")
        self.assertEqual(creada.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            self.client.delete(f"/api/categorias/{creada.data['id']}/").status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_busqueda_y_ordenamiento_de_espacios(self):
        busqueda = self.client.get("/api/espacios/", {"search": "central"})
        self.assertEqual([e["nombre"] for e in busqueda.data], ["Biblioteca"])

        orden = self.client.get("/api/espacios/", {"ordering": "-aforo"})
        self.assertEqual([e["nombre"] for e in orden.data], ["Biblioteca", "Aula 201", "Laboratorio 3"])

    def test_solicitantes_anidados_y_optimizados(self):
        with self.assertNumQueries(3):
            respuesta = self.client.get("/api/solicitantes/")
        ana = next(s for s in respuesta.data if s["codigo"] == "U20261234")
        self.assertEqual(ana["perfil"]["documento_identidad"], "71234567")
        self.assertIn("Biblioteca", [a["espacio"] for a in ana["autorizaciones"]])

        docentes = self.client.get("/api/solicitantes/", {"rol": "docente"})
        self.assertEqual([s["nombre"] for s in docentes.data], ["Carlos Medina"])

    def test_prestamos_filtro_estado_y_acciones(self):
        hoy = timezone.localdate()
        Prestamo.objects.create(
            codigo="PR-900",
            nombre_solicitante="Prueba API",
            fecha_prestamo=hoy,
            fecha_estimada_devolucion=hoy + timedelta(days=7),
            estado="devuelto",
        )

        with self.assertNumQueries(2):
            todos = self.client.get("/api/prestamos/")
        pr001 = next(p for p in todos.data if p["codigo"] == "PR-001")
        self.assertEqual(len(pr001["detalles"]), DetallePrestamo.objects.filter(prestamo__codigo="PR-001").count())

        activos = self.client.get("/api/prestamos/", {"estado": "activo"})
        self.assertEqual([p["codigo"] for p in activos.data], ["PR-001"])

        accion_activos = self.client.get("/api/prestamos/activos/")
        self.assertEqual([p["codigo"] for p in accion_activos.data], ["PR-001"])

        del_mes = self.client.get("/api/prestamos/del-mes/")
        self.assertIn("PR-900", [p["codigo"] for p in del_mes.data])

        combinado = self.client.get("/api/prestamos/del-mes/", {"estado": "activo"})
        self.assertNotIn("PR-900", [p["codigo"] for p in combinado.data])

        self.assertEqual(self.client.delete("/api/prestamos/1/").status_code, 405)
