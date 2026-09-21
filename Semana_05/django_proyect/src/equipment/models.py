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


class FichaTecnica(models.Model):
    """Ficha complementaria 1:1. Solo existe si existe el equipo, y como máximo una."""

    equipo = models.OneToOneField(
        Equipo,
        on_delete=models.CASCADE,
        related_name="ficha",
    )
    numero_serie = models.CharField(max_length=80)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    garantia_hasta = models.DateField(null=True, blank=True)
    especificaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "ficha técnica"
        verbose_name_plural = "fichas técnicas"

    def __str__(self):
        return f"Ficha de {self.equipo.nombre}"


class Mantenimiento(models.Model):
    """Un equipo tiene muchos mantenimientos. La FK vive en el lado 'muchos'."""

    TIPOS = [
        ("preventivo", "Preventivo"),
        ("correctivo", "Correctivo"),
    ]

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="mantenimientos",
    )
    fecha = models.DateField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    tecnico = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"{self.equipo.nombre} — {self.fecha}"


class Accesorio(models.Model):
    nombre = models.CharField(max_length=80)
    tipo = models.CharField(max_length=50)
    equipos = models.ManyToManyField(
        Equipo,
        through="AsignacionAccesorio",
        related_name="accesorios",
        blank=True,
    )

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class AsignacionAccesorio(models.Model):
    """Relación N:M Equipo–Accesorio con datos propios (cantidad, fecha, estado)."""

    ESTADOS = [
        ("vigente", "Vigente"),
        ("devuelto", "Devuelto"),
        ("perdido", "Perdido"),
    ]

    equipo = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="asignaciones_accesorio",
    )
    accesorio = models.ForeignKey(
        Accesorio,
        on_delete=models.CASCADE,
        related_name="asignaciones",
    )
    cantidad = models.PositiveIntegerField(default=1)
    fecha_asignacion = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="vigente")

    class Meta:
        ordering = ["-fecha_asignacion"]
        verbose_name = "asignación de accesorio"
        verbose_name_plural = "asignaciones de accesorio"

    def __str__(self):
        return f"{self.accesorio} → {self.equipo} ({self.cantidad})"
