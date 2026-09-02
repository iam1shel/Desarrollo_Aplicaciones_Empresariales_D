from django.test import TestCase
from django.urls import reverse
from .models import Equipo


class EquipoPersistenciaTests(TestCase):
    def test_listado_muestra_equipos_sembrados(self):
        respuesta = self.client.get(reverse("equipo_list"))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Laptop 01")
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
