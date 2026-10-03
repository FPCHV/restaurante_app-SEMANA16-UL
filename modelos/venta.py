from datetime import datetime


class Venta:
    """Representa una venta sencilla entre un usuario y un producto."""

    def __init__(self, id, usuario_id, producto_id, fecha=None):
        self.id = int(id)
        self.usuario_id = int(usuario_id)
        self.producto_id = int(producto_id)
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "producto_id": self.producto_id,
            "fecha": self.fecha,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
