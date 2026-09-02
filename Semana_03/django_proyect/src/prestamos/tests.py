from django.test import TestCase
from django.urls import reverse
from .models import Categoria, DetallePrestamo, Prestamo


class PrestamosCrudTests(TestCase):
    def test_home_y_listados(self):
        for nombre in [
            "prestamos_home",
            "categoria_list",
            "espacio_list",
            "solicitante_list",
            "prestamo_list",
            "detalle_list",
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
