class Producto:
    def __init__(self, id, nombre, precio, cantidad):
        self.id = int(id)
        self.nombre = str(nombre)
        self.precio = float(precio)
        self.cantidad = int(cantidad)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "precio": self.precio,
            "cantidad": self.cantidad,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
