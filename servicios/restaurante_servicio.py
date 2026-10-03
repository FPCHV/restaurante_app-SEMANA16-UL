from pathlib import Path
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    """Contiene las reglas del restaurante y delega la persistencia a ArchivoServicio."""

    def __init__(self, archivo_servicio):
        self.archivo_servicio = archivo_servicio
        self.base_dir = Path(__file__).resolve().parent.parent
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self.usuario_actual = None  # Usuario autenticado en la sesión vigente
        self.cargar_datos()

    def cargar_datos(self):
        u = self.archivo_servicio.leer_json(
            self.base_dir / "datos" / "usuarios.json"
        )
        p = self.archivo_servicio.leer_json(
            self.base_dir / "datos" / "productos.json"
        )
        ruta_ventas = self.base_dir / "datos" / "ventas.json"

        self.usuarios = [Usuario.from_dict(x) for x in u]
        self.productos = [Producto.from_dict(x) for x in p]

        if ruta_ventas.exists():
            ventas = self.archivo_servicio.leer_json(ruta_ventas)
        else:
            ventas = []
            self.archivo_servicio.guardar_json(ruta_ventas, ventas)

        self.ventas = [Venta.from_dict(x) for x in ventas]

    # ---------- Acceso y sesión ----------
    def autenticar(self, usuario, contrasena):
        """Devuelve el Usuario que coincide con las credenciales o None."""
        return next(
            (x for x in self.usuarios
             if x.usuario == usuario and x.contrasena == contrasena),
            None,
        )

    def validar_acceso(self, usuario, contrasena):
        return self.autenticar(usuario, contrasena) is not None

    def iniciar_sesion(self, usuario, contrasena):
        """Valida las credenciales y conserva al usuario autenticado."""
        self.usuario_actual = self.autenticar(usuario, contrasena)
        return self.usuario_actual is not None

    def cerrar_sesion(self):
        self.usuario_actual = None

    def es_administrador(self):
        return self.usuario_actual is not None and self.usuario_actual.es_administrador

    def _exigir_administrador(self):
        if not self.es_administrador():
            raise PermissionError(
                "Solo el usuario con rol Administrador puede gestionar usuarios."
            )

    # ---------- Usuarios ----------
    def listar_usuarios(self):
        return self.usuarios

    def buscar_usuario(self, id_usuario):
        try:
            id_usuario = int(id_usuario)
        except (TypeError, ValueError):
            return None
        return next((u for u in self.usuarios if u.id == id_usuario), None)

    def listar_roles_gestionables(self):
        """Roles que el administrador puede asignar desde la interfaz."""
        return [Usuario.ROL_EMPLEADO, Usuario.ROL_CLIENTE]

    def descripcion_rol(self, rol):
        return Usuario.ROLES.get(rol, "")

    def contar_por_rol(self, rol):
        return sum(1 for u in self.usuarios if u.rol == rol)

    def registrar_usuario(self, nombre, usuario, contrasena, rol):
        """Crea un Empleado o Cliente con un ID generado automáticamente."""
        self._exigir_administrador()
        self._validar_usuario(nombre, usuario, rol)
        self._validar_contrasena(contrasena)
        self._validar_usuario_unico(usuario)

        nuevo_id = max((u.id for u in self.usuarios), default=0) + 1
        nuevo = Usuario(nuevo_id, usuario.strip(), contrasena, nombre.strip(), rol)
        self.usuarios.append(nuevo)
        self._guardar_usuarios()
        return nuevo

    def actualizar_usuario(self, id_usuario, nombre, usuario, contrasena, rol):
        """Actualiza un Empleado o Cliente. Contraseña vacía = conservar la actual."""
        self._exigir_administrador()
        existente = self._obtener_gestionable(id_usuario, "actualizar")
        self._validar_usuario(nombre, usuario, rol)
        if contrasena:
            self._validar_contrasena(contrasena)
        self._validar_usuario_unico(usuario, ignorar_id=existente.id)

        existente.nombre = nombre.strip()
        existente.usuario = usuario.strip()
        existente.rol = rol
        if contrasena:
            existente.contrasena = contrasena
        self._guardar_usuarios()
        return existente

    def validar_eliminacion_usuario(self, id_usuario):
        """Comprueba si se puede eliminar; la interfaz lo usa antes de confirmar."""
        self._exigir_administrador()
        return self._obtener_gestionable(id_usuario, "eliminar")

    def eliminar_usuario(self, id_usuario):
        existente = self.validar_eliminacion_usuario(id_usuario)
        self.usuarios = [u for u in self.usuarios if u.id != existente.id]
        self._guardar_usuarios()
        return existente

    def _obtener_gestionable(self, id_usuario, accion):
        existente = self.buscar_usuario(id_usuario)
        if not existente:
            raise ValueError(f"No se encontró el usuario para {accion}.")
        if self.usuario_actual and existente.id == self.usuario_actual.id:
            raise ValueError(
                f"No puede {accion} la cuenta con la que inició sesión."
            )
        if existente.es_administrador:
            raise ValueError(
                "Las cuentas de Administrador no se gestionan desde esta pantalla."
            )
        return existente

    def _guardar_usuarios(self):
        ruta = self.base_dir / "datos" / "usuarios.json"
        self.archivo_servicio.guardar_json(
            ruta, [u.to_dict() for u in self.usuarios]
        )

    def _validar_usuario_unico(self, usuario, ignorar_id=None):
        clave = usuario.strip().lower()
        if any(u.usuario.lower() == clave and u.id != ignorar_id for u in self.usuarios):
            raise ValueError("Ya existe un usuario con ese nombre de usuario.")

    def _validar_usuario(self, nombre, usuario, rol):
        if not str(nombre).strip():
            raise ValueError("El nombre es obligatorio.")
        usuario = str(usuario).strip()
        if len(usuario) < 3:
            raise ValueError("El usuario debe tener al menos 3 caracteres.")
        if " " in usuario:
            raise ValueError("El usuario no puede contener espacios.")
        if rol not in self.listar_roles_gestionables():
            raise ValueError("Seleccione un rol válido: Empleado o Cliente.")

    @staticmethod
    def _validar_contrasena(contrasena):
        if len(str(contrasena)) < 4:
            raise ValueError("La contraseña debe tener al menos 4 caracteres.")

    # ---------- Productos ----------
    def listar_productos(self):
        return self.productos

    def buscar_producto(self, id_producto):
        try:
            id_producto = int(id_producto)
        except (TypeError, ValueError):
            return None
        return next((p for p in self.productos if p.id == id_producto), None)

    def registrar_producto(self, id_producto, nombre, precio, cantidad):
        self._validar_producto(id_producto, nombre, precio, cantidad)
        if self.buscar_producto(id_producto):
            raise ValueError("Ya existe un producto con ese ID.")

        producto = Producto(
            int(id_producto), nombre.strip(), float(precio), int(cantidad)
        )
        self.productos.append(producto)
        self._guardar_productos()
        return producto

    def actualizar_producto(self, id_producto, nombre, precio, cantidad):
        self._validar_producto(id_producto, nombre, precio, cantidad)
        producto = self.buscar_producto(id_producto)
        if not producto:
            raise ValueError("No se encontró el producto para actualizar.")

        producto.nombre = nombre.strip()
        producto.precio = float(precio)
        producto.cantidad = int(cantidad)
        self._guardar_productos()
        return producto

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto(id_producto)
        if not producto:
            raise ValueError("No se encontró el producto para eliminar.")

        self.productos = [p for p in self.productos if p.id != producto.id]
        self._guardar_productos()
        return producto

    def _guardar_productos(self):
        ruta = self.base_dir / "datos" / "productos.json"
        self.archivo_servicio.guardar_json(
            ruta, [p.to_dict() for p in self.productos]
        )

    # ---------- Ventas ----------
    def listar_ventas(self):
        return self.ventas

    def registrar_venta(self, usuario_id, producto_id):
        """Valida usuario y producto y registra una venta en ventas.json."""
        usuario = self.buscar_usuario(usuario_id)
        if not usuario:
            raise ValueError("El usuario seleccionado no existe.")

        producto = self.buscar_producto(producto_id)
        if not producto:
            raise ValueError("El producto seleccionado no existe.")

        if producto.cantidad <= 0:
            raise ValueError("El producto seleccionado no tiene stock disponible.")

        nuevo_id = max((v.id for v in self.ventas), default=0) + 1
        venta = Venta(nuevo_id, usuario.id, producto.id)

        # Una venta representa una unidad del producto seleccionado.
        producto.cantidad -= 1
        self.ventas.append(venta)

        self._guardar_productos()
        self._guardar_ventas()
        return venta

    def _guardar_ventas(self):
        ruta = self.base_dir / "datos" / "ventas.json"
        self.archivo_servicio.guardar_json(
            ruta, [v.to_dict() for v in self.ventas]
        )

    @staticmethod
    def _validar_producto(id_producto, nombre, precio, cantidad):
        try:
            id_producto = int(id_producto)
        except (TypeError, ValueError):
            raise ValueError("El ID debe ser un número entero.")

        if id_producto <= 0:
            raise ValueError("El ID debe ser mayor que cero.")

        if not str(nombre).strip():
            raise ValueError("El nombre es obligatorio.")

        try:
            precio = float(precio)
        except (TypeError, ValueError):
            raise ValueError("El precio debe ser numérico.")

        if precio < 0:
            raise ValueError("El precio no puede ser negativo.")

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número entero.")

        if cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
