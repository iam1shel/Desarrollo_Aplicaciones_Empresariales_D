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
    espacios = models.ManyToManyField(
        Espacio,
        through="AutorizacionEspacio",
        related_name="solicitantes",
        blank=True,
    )

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


class PerfilSolicitante(models.Model):
    """Ficha 1:1 del solicitante. No son más campos de Solicitante: es opcional
    y concentra datos de contacto institucional que no todo registro tiene."""

    solicitante = models.OneToOneField(
        Solicitante,
        on_delete=models.CASCADE,
        related_name="perfil",
    )
    documento_identidad = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20, blank=True)
    area_o_ciclo = models.CharField("Área o ciclo", max_length=80, blank=True)
    observaciones = models.TextField(blank=True)

    class Meta:
        verbose_name = "perfil de solicitante"
        verbose_name_plural = "perfiles de solicitante"

    def __str__(self):
        return f"Perfil de {self.solicitante.nombre}"


class AutorizacionEspacio(models.Model):
    """N:M Solicitante–Espacio. Fecha de vigencia y estado pertenecen a la
    autorización, no a la persona ni al aula."""

    ESTADOS = [
        ("vigente", "Vigente"),
        ("vencida", "Vencida"),
        ("revocada", "Revocada"),
    ]

    solicitante = models.ForeignKey(
        Solicitante,
        on_delete=models.CASCADE,
        related_name="autorizaciones",
    )
    espacio = models.ForeignKey(
        Espacio,
        on_delete=models.CASCADE,
        related_name="autorizaciones",
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="vigente")

    class Meta:
        ordering = ["-fecha_inicio"]
        verbose_name = "autorización de espacio"
        verbose_name_plural = "autorizaciones de espacio"

    def __str__(self):
        return f"{self.solicitante.nombre} → {self.espacio.nombre}"
