class Usuario:
    """Representa a una persona registrada en el restaurante.

    El atributo ``rol`` diferencia de forma sencilla entre Administrador,
    Empleado y Cliente.
    """

    ROL_ADMINISTRADOR = "Administrador"
    ROL_EMPLEADO = "Empleado"
    ROL_CLIENTE = "Cliente"

    # Descripción breve de cada rol (la interfaz la muestra al elegir un rol).
    ROLES = {
        ROL_ADMINISTRADOR: "Gestiona usuarios y opera todo el sistema.",
        ROL_EMPLEADO: "Personal del restaurante: atiende productos y ventas.",
        ROL_CLIENTE: "Comensal registrado: puede comprar en el restaurante.",
    }

    def __init__(self, id, usuario, contrasena, nombre, rol=ROL_CLIENTE):
        self.id = int(id)
        self.usuario = str(usuario)
        self.contrasena = str(contrasena)
        self.nombre = str(nombre)
        self.rol = str(rol)

    @property
    def es_administrador(self):
        return self.rol == self.ROL_ADMINISTRADOR

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "contrasena": self.contrasena,
            "nombre": self.nombre,
            "rol": self.rol,
        }

    @classmethod
    def from_dict(cls, data):
        # Los archivos de semanas anteriores no tenían "rol": se asigna Cliente
        # por defecto para no romper la compatibilidad con datos antiguos.
        return cls(
            data["id"],
            data["usuario"],
            data["contrasena"],
            data["nombre"],
            data.get("rol", cls.ROL_CLIENTE),
        )
