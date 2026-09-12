from django.test import TestCase
from django.urls import reverse
from .models import AutorizacionEspacio, Categoria, DetallePrestamo, Espacio, Prestamo, Solicitante


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
