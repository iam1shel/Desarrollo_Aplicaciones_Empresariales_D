from django.db import models


class Categoria(models.Model):
    nombre = models.CharField(max_length=80)
    descripcion = models.TextField(blank=True)

    class Meta:
        ordering = ["nombre"]
        verbose_name = "categoría"
        verbose_name_plural = "categorías"

    def __str__(self):
        return self.nombre


class Espacio(models.Model):
    nombre = models.CharField(max_length=80)
    edificio = models.CharField(max_length=80)
    piso = models.CharField(max_length=20, blank=True)
    aforo = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.edificio})"


class Solicitante(models.Model):
    ROLES = [
        ("estudiante", "Estudiante"),
        ("docente", "Docente"),
        ("personal", "Personal"),
    ]

    nombre = models.CharField(max_length=120)
    codigo = models.CharField("Código institucional", max_length=20, unique=True)
    rol = models.CharField(max_length=20, choices=ROLES)
    correo = models.EmailField(blank=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class Prestamo(models.Model):
    ESTADOS = [
        ("activo", "Activo"),
        ("devuelto", "Devuelto"),
        ("atrasado", "Atrasado"),
    ]

    codigo = models.CharField(max_length=20, unique=True)
    nombre_solicitante = models.CharField(max_length=120)
    fecha_prestamo = models.DateField()
    fecha_estimada_devolucion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="activo")
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ["-fecha_prestamo"]
        verbose_name = "préstamo"
        verbose_name_plural = "préstamos"

    def __str__(self):
        return self.codigo


class DetallePrestamo(models.Model):
    prestamo = models.ForeignKey(
        Prestamo,
        on_delete=models.CASCADE,
        related_name="detalles",
    )
    nombre_equipo = models.CharField(max_length=100)
    cantidad = models.PositiveIntegerField(default=1)
    observacion = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["id"]
        verbose_name = "detalle de préstamo"
        verbose_name_plural = "detalles de préstamo"

    def __str__(self):
        return f"{self.nombre_equipo} x{self.cantidad} ({self.prestamo.codigo})"
