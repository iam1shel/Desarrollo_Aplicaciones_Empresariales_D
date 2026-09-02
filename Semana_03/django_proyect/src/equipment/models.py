from django.db import models


class Equipo(models.Model):
    ESTADOS = [
        ("disponible", "Disponible"),
        ("prestado", "Prestado"),
    ]

    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50)
    marca = models.CharField(max_length=50)
    ubicacion = models.CharField(max_length=100)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="disponible")
    descripcion = models.TextField(blank=True)
    prestado_a = models.CharField("Quién lo tiene", max_length=100, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.nombre
