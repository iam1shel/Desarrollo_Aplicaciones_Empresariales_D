class Equipo:
    def __init__(self, id,nombre, tipo, marca, ubicacion, estado, descripcion="", prestado_a=""):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo
        self.marca = marca
        self.ubicacion = ubicacion
        self.estado = estado
        self.descripcion = descripcion
        self.prestado_a = prestado_a

equipos = [
    Equipo(1, "Laptop 01", "Laptop", "Lenovo", "Biblioteca", "disponible", "Uso en sala de estudio"),
    Equipo(2, "Proyector 01", "Proyector", "Epson", "Aula 201", "prestado", ""),
    Equipo(3, "Mouse 01", "Mouse", "Acer", "Aula 1501", "prestado", ""),
    Equipo(4, "Laptop 02", "Laptop", "HP", "Biblioteca", "disponible", "Uso en sala de estudio"),
    Equipo(5, "Tablet 01", "Tablet", "Honor", "Aula 505", "prestado", ""),

]