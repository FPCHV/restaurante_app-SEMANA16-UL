# Restaurante App — Semana 16

## Manejo de eventos en Tkinter: gestión de usuarios

Esta versión continúa el proyecto de la Semana 15 sin reconstruirlo. Se conservan el inicio de sesión, la navegación, la gestión de productos, las ventas, la persistencia en JSON y la arquitectura modular. La evolución de esta semana se concentra en la sección **Usuarios**, que ahora permite **registrar, consultar, actualizar y eliminar** usuarios aplicando eventos de Tkinter:

**Interacción del usuario → evento → `bind()` → callback → `RestauranteServicio` → persistencia (`usuarios.json`) → respuesta visual.**

## Evolución respecto a la Semana 15

| Elemento | Semana 15 | Semana 16 |
|---|---|---|
| Modelo `Usuario` | id, usuario, contraseña, nombre | Se agrega el atributo **`rol`** (Administrador, Empleado, Cliente) |
| `usuarios.json` | Sin rol | Incluye `rol` en cada registro |
| `RestauranteServicio` | Solo listar/buscar usuarios | Registrar, actualizar y eliminar usuarios, validaciones, sesión y control de acceso por rol |
| Sección Usuarios | Tabla de solo consulta | Formulario + Treeview con CRUD y eventos |
| `LoginView` | Solo botón Ingresar | Se agrega `<Return>` en los campos de acceso |
| `assets/` | Logo e íconos de navegación | Logo e íconos a color (naranja, café y crema) y nuevos íconos de Registrar, Actualizar, Eliminar, Limpiar y Administrador |
| `ui/` | Estilos definidos en `MainView` | Nuevo módulo `ui/tema.py` con la paleta y los estilos compartidos por login y panel principal |

Productos y Ventas no cambian su funcionamiento.

## Roles

| Rol | Descripción | Acceso a "Usuarios" |
|---|---|---|
| Administrador | Gestiona usuarios y opera todo el sistema | Sí |
| Empleado | Personal del restaurante: productos y ventas | No |
| Cliente | Comensal registrado | No |

- El botón **Usuarios** solo aparece para el Administrador. Además, `RestauranteServicio` rechaza (`PermissionError`) cualquier operación de gestión si la sesión no es de un Administrador, de modo que la regla no depende solo de la interfaz.
- El administrador gestiona usuarios de tipo **Empleado** y **Cliente** (son los roles que ofrece el Combobox). Las cuentas de Administrador se muestran en la tabla, pero no se editan ni eliminan desde esta pantalla.
- La cuenta con la que se inició sesión **no puede eliminarse**: el servicio lo impide y la interfaz muestra el motivo sin pedir confirmación.
- No se implementa un sistema complejo de permisos.

## Gestión de usuarios

- **Registrar:** el ID se genera automáticamente (máximo existente + 1). Se valida nombre obligatorio, usuario de al menos 3 caracteres sin espacios y no repetido, contraseña de al menos 4 caracteres y rol válido.
- **Consultar:** el Treeview muestra `ID`, `Nombre completo`, `Usuario` y `Rol`. **La contraseña nunca se muestra** ni se carga en el formulario.
- **Actualizar:** modifica nombre, usuario y rol. Si el campo contraseña se deja vacío se conserva la actual.
- **Eliminar:** pide confirmación con `askyesno` antes de borrar.
- Tarjetas de resumen con el total de usuarios y la cantidad por rol.

## Eventos implementados

| Evento | Widget | Callback | Qué hace |
|---|---|---|---|
| `<<TreeviewSelect>>` | Treeview de usuarios | `_on_usuario_seleccionado` | Lee el ID de la fila, consulta `servicio.buscar_usuario()` y carga los datos en el formulario |
| `<Return>` | Campos del formulario | `_on_return_registrar` | Llama a `registrar_usuario()` (el mismo método del botón Registrar) |
| `<Escape>` | Formulario, tabla y botones | `_on_escape_limpiar` | Llama a `limpiar_formulario_usuario()`: vacía el formulario, quita la selección y vuelve al estado inicial |
| `<<ComboboxSelected>>` | Combobox de rol | `_on_rol_seleccionado` | Muestra la descripción del rol elegido y lo indica en la barra de estado |
| `<Return>` | Campos del login | `_on_return_ingresar` | Llama a `ingresar()` (el mismo método del botón Ingresar) |

### `bind()`, `command=` y callbacks

- **`command=`** se usa en los botones **Registrar, Actualizar, Eliminar y Limpiar**: asocia directamente el clic con un método (`command=self.registrar_usuario`, sin paréntesis).
- **`bind()`** se usa para eventos que un botón no cubre: selección en una tabla, teclas y cambio de opción en un Combobox. El callback recibe el objeto `event`.
- Los callbacks de `bind()` **no repiten lógica**: `<Return>` y `<Escape>` solo invocan los mismos métodos que usan los botones (`registrar_usuario`, `limpiar_formulario_usuario`). Así hay una única implementación de cada operación.
- La interfaz solo captura la interacción, lee/actualiza widgets y muestra mensajes. Las validaciones, reglas y persistencia están en `RestauranteServicio`.

## Persistencia

`ArchivoServicio` lee y escribe JSON. `RestauranteServicio` decide qué guardar y cuándo:

- `main_view.py` → interacción y presentación (no abre archivos JSON).
- `restaurante_servicio.py` → reglas, validaciones, sesión y operaciones.
- `archivo_servicio.py` → lectura y escritura de JSON.
- `datos/*.json` → `usuarios.json`, `productos.json`, `ventas.json`.

Cada registro de `usuarios.json` incluye `rol`. Si un archivo antiguo no lo tuviera, el modelo asigna `Cliente` por defecto.

## Estructura del proyecto

```text
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   ├── main_view.py
│   └── tema.py
├── assets/
│   ├── logo_restaurante.png
│   ├── icono_productos.png
│   ├── icono_usuarios.png
│   ├── icono_ventas.png
│   ├── icono_registrar.png
│   ├── icono_actualizar.png
│   ├── icono_eliminar.png
│   ├── icono_limpiar.png
│   ├── icono_administrador.png
│   └── README.txt
├── main.py
└── README.md
```

## Recursos visuales (`assets/`)

La paleta del sistema (naranja `#D35400`, rojo oscuro `#8B2A1A`, crema `#F4ECE2` y café `#3C281E`) se define una sola vez en `ui/tema.py` y se aplica a login, navegación, botones, formularios y tablas. El logo se muestra en el login y en el encabezado. Los íconos se usan en la navegación (Productos, Usuarios, Ventas), en los botones de gestión de usuarios y en el indicador de sesión (nombre y rol del usuario autenticado).

## Credenciales de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `1234` | Administrador |
| `mesero` | `1234` | Empleado |
| `cliente` | `1234` | Cliente |

## Ejecución

Requiere Python 3.8+ con Tkinter (incluido en la instalación estándar). Desde la carpeta `restaurante_app`:

```bash
python main.py
```

## Comprobación de funcionamiento

1. Ejecutar `main.py` e iniciar sesión con `admin` / `1234` (también funciona Enter en el login).
2. Verificar que Productos y Ventas siguen funcionando.
3. Abrir **Usuarios** (solo visible para el Administrador).
4. Registrar un Empleado o Cliente con el botón **Registrar** y verlo en la tabla.
5. Seleccionar una fila: `<<TreeviewSelect>>` carga sus datos en el formulario.
6. Cambiar un dato y pulsar **Actualizar**.
7. Pulsar **Limpiar** o la tecla **Esc**: se vacía el formulario y se quita la selección.
8. Llenar el formulario y pulsar **Enter**: se ejecuta el registro.
9. Cambiar el rol en el Combobox: aparece la descripción del rol (`<<ComboboxSelected>>`).
10. Seleccionar un usuario y pulsar **Eliminar**: pide confirmación.
11. Seleccionar `admin` (sesión actual) y pulsar **Eliminar**: la aplicación lo impide.
12. Cerrar sesión e ingresar con `mesero` o `cliente`: el botón Usuarios no aparece.
13. Cerrar y volver a ejecutar: los usuarios se recuperan desde `usuarios.json`.

## Fuera del alcance de esta semana

Bloqueo o suspensión de cuentas, recuperación de contraseña, permisos avanzados, base de datos, cifrado y administración compleja de roles.
