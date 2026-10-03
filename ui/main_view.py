import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from modelos.usuario import Usuario
from ui import tema
from ui.tema import aplicar_tema


class MainView:
    """Interfaz principal del restaurante.

    La vista organiza navegación, formularios, acciones y tablas sin asumir
    la lógica de negocio. Las operaciones se delegan a RestauranteServicio.
    """

    def __init__(self, root, servicio, on_logout):
        self.root = root
        self.servicio = servicio
        self.on_logout = on_logout
        self.frame = ttk.Frame(root, padding=18)

        self._configurar_estilos()
        self._cargar_recursos()
        self._construir_encabezado()
        self._construir_navegacion()

        self.contenido = ttk.Frame(self.frame, style="Content.TFrame")
        self.contenido.pack(fill="both", expand=True)
        self.productos()

    def _configurar_estilos(self):
        aplicar_tema(self.root)

    def _cargar_recursos(self):
        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        self.logo = self._cargar_imagen(assets_dir / "logo_restaurante.png", 3)
        self.icono_productos = self._cargar_imagen(assets_dir / "icono_productos.png", 4)
        self.icono_usuarios = self._cargar_imagen(assets_dir / "icono_usuarios.png", 4)
        self.icono_ventas = self._cargar_imagen(assets_dir / "icono_ventas.png", 4)
        self.icono_registrar = self._cargar_imagen(assets_dir / "icono_registrar.png", 6)
        self.icono_actualizar = self._cargar_imagen(assets_dir / "icono_actualizar.png", 6)
        self.icono_eliminar = self._cargar_imagen(assets_dir / "icono_eliminar.png", 6)
        self.icono_limpiar = self._cargar_imagen(assets_dir / "icono_limpiar.png", 6)
        self.icono_admin = self._cargar_imagen(assets_dir / "icono_administrador.png", 6)
        self.icono_sesion = self._cargar_imagen(assets_dir / "icono_usuarios.png", 6)

    @staticmethod
    def _cargar_imagen(path, divisor):
        try:
            imagen = tk.PhotoImage(file=str(path))
            if divisor > 1:
                imagen = imagen.subsample(divisor, divisor)
            return imagen
        except tk.TclError:
            return None

    def _construir_encabezado(self):
        encabezado = ttk.Frame(self.frame, style="Header.TFrame", padding=(14, 10))
        encabezado.pack(fill="x", pady=(0, 10))

        if self.logo:
            ttk.Label(encabezado, image=self.logo, style="Header.TLabel").pack(
                side="left", padx=(0, 12)
            )

        textos = ttk.Frame(encabezado, style="Header.TFrame")
        textos.pack(side="left", fill="x", expand=True)
        ttk.Label(
            textos,
            text="RESTAURANTE APP",
            style="Title.TLabel",
            background=tema.TARJETA
        ).pack(anchor="w")
        ttk.Label(
            textos,
            text="Sistema de gestión de productos, usuarios y ventas · Semana 16",
            style="Subtitle.TLabel",
            background=tema.TARJETA
        ).pack(anchor="w", pady=(2, 0))

        ttk.Button(
            encabezado,
            text="Cerrar sesión",
            command=self.on_logout,
            style="Action.TButton"
        ).pack(side="right")

        # Muestra quién inició sesión y con qué rol (se actualiza en _aplicar_permisos).
        self.sesion_label = ttk.Label(
            encabezado, text="", compound="left",
            font=("Segoe UI", 9, "bold"), style="Header.TLabel"
        )
        self.sesion_label.pack(side="right", padx=14)

    def _construir_navegacion(self):
        navegacion = ttk.Frame(self.frame, style="Nav.TFrame", padding=(8, 8))
        navegacion.pack(fill="x", pady=(0, 12))

        ttk.Label(
            navegacion,
            text="MENÚ PRINCIPAL",
            style="Nav.TLabel"
        ).pack(side="left", padx=(6, 12))

        self.btn_productos = ttk.Button(
            navegacion, text="Productos", image=self.icono_productos,
            compound="left", command=self.productos, style="Nav.TButton"
        )
        self.btn_productos.pack(side="left", padx=4)

        self.btn_usuarios = ttk.Button(
            navegacion, text="Usuarios", image=self.icono_usuarios,
            compound="left", command=self.usuarios, style="Nav.TButton"
        )
        self.btn_usuarios.pack(side="left", padx=4)

        self.btn_ventas = ttk.Button(
            navegacion, text="Ventas", image=self.icono_ventas,
            compound="left", command=self.ventas, style="Nav.TButton"
        )
        self.btn_ventas.pack(side="left", padx=4)

        self.estado = ttk.Label(navegacion, text="Productos", style="Nav.TLabel")
        self.estado.pack(side="right", padx=10)

    def _aplicar_permisos(self):
        """Adapta la interfaz al rol de la sesión: solo el Administrador ve Usuarios."""
        usuario = self.servicio.usuario_actual
        if usuario:
            icono = self.icono_admin if usuario.es_administrador else self.icono_sesion
            self.sesion_label.config(
                text=f"{usuario.nombre} · {usuario.rol}", image=icono or ""
            )
        if self.servicio.es_administrador():
            self.btn_usuarios.pack(side="left", padx=4, before=self.btn_ventas)
        else:
            self.btn_usuarios.pack_forget()

    def _limpiar_contenido(self):
        for widget in self.contenido.winfo_children():
            widget.destroy()

    def _titulo_seccion(self, titulo, descripcion):
        cabecera = ttk.Frame(self.contenido)
        cabecera.pack(fill="x", pady=(0, 10))
        ttk.Label(cabecera, text=titulo, style="Section.TLabel").pack(anchor="w")
        ttk.Label(cabecera, text=descripcion, style="Subtitle.TLabel").pack(anchor="w", pady=(2, 0))

    def _tarjeta_resumen(self, parent, columna, titulo, valor):
        card = ttk.LabelFrame(parent, text=titulo, padding=(12, 8))
        card.grid(row=0, column=columna, sticky="nsew", padx=4)
        card.valor = ttk.Label(card, text=str(valor), style="CardValue.TLabel")
        card.valor.pack(anchor="w")
        parent.columnconfigure(columna, weight=1)
        return card

    # ---------- Productos ----------
    def productos(self):
        self.estado.config(text="Sección activa: Productos")
        self._limpiar_contenido()
        self._titulo_seccion(
            "Gestión de productos",
            "Registre, consulte, actualice y elimine los productos del restaurante."
        )

        resumen = ttk.Frame(self.contenido)
        resumen.pack(fill="x", pady=(0, 10))
        productos = self.servicio.listar_productos()
        stock = sum(p.cantidad for p in productos)
        self._tarjeta_resumen(resumen, 0, "Productos registrados", len(productos))
        self._tarjeta_resumen(resumen, 1, "Unidades en stock", stock)
        self._tarjeta_resumen(resumen, 2, "Precio promedio", self._precio_promedio(productos))

        formulario = ttk.LabelFrame(self.contenido, text="Datos del producto", padding=12)
        formulario.pack(fill="x", pady=(0, 10))

        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.precio_var = tk.StringVar()
        self.cantidad_var = tk.StringVar()

        campos = [
            ("ID", self.id_var),
            ("Nombre", self.nombre_var),
            ("Precio", self.precio_var),
            ("Cantidad", self.cantidad_var),
        ]
        for col, (texto, variable) in enumerate(campos):
            formulario.columnconfigure(col, weight=1)
            ttk.Label(formulario, text=texto).grid(row=0, column=col, sticky="w", padx=5)
            ttk.Entry(formulario, textvariable=variable).grid(
                row=1, column=col, sticky="ew", padx=5, pady=(4, 2)
            )

        acciones = ttk.Frame(self.contenido)
        acciones.pack(fill="x", pady=(0, 10))
        for texto, icono, comando in [
            ("Registrar", self.icono_registrar, self.registrar),
            ("Cargar / Consultar", None, self.cargar),
            ("Actualizar", self.icono_actualizar, self.actualizar),
            ("Eliminar", self.icono_eliminar, self.eliminar),
            ("Limpiar", self.icono_limpiar, self.limpiar_formulario),
        ]:
            ttk.Button(
                acciones, text=texto, image=icono or "", compound="left", command=comando,
                style="Danger.TButton" if texto == "Eliminar" else "Action.TButton"
            ).pack(side="left", padx=(0, 6))

        tabla_frame = ttk.LabelFrame(self.contenido, text="Productos registrados", padding=8)
        tabla_frame.pack(fill="both", expand=True)
        self.tree = ttk.Treeview(
            tabla_frame, columns=("id", "nombre", "precio", "cantidad"), show="headings"
        )
        for c, h, w in [
            ("id", "ID", 90), ("nombre", "Producto", 320),
            ("precio", "Precio", 140), ("cantidad", "Cantidad", 140)
        ]:
            self.tree.heading(c, text=h)
            self.tree.column(c, width=w, anchor="center")
        scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self._refrescar_tabla()

    @staticmethod
    def _precio_promedio(productos):
        if not productos:
            return "$0.00"
        return f"${sum(p.precio for p in productos) / len(productos):.2f}"

    def _refrescar_tabla(self):
        if not hasattr(self, "tree") or not self.tree.winfo_exists():
            return
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in self.servicio.listar_productos():
            self.tree.insert("", "end", values=(p.id, p.nombre, f"${p.precio:.2f}", p.cantidad))
        self.estado.config(text="Productos actualizados")

    def registrar(self):
        try:
            p = self.servicio.registrar_producto(
                self.id_var.get(), self.nombre_var.get(),
                self.precio_var.get(), self.cantidad_var.get()
            )
            self._refrescar_tabla()
            self.limpiar_formulario()
            messagebox.showinfo("Registro", f"Producto '{p.nombre}' registrado correctamente.")
        except ValueError as e:
            messagebox.showerror("Registro", str(e))

    def cargar(self):
        p = self.servicio.buscar_producto(self.id_var.get())
        if not p:
            messagebox.showwarning("Consulta", "No se encontró un producto con ese ID.")
            return
        self.nombre_var.set(p.nombre)
        self.precio_var.set(str(p.precio))
        self.cantidad_var.set(str(p.cantidad))
        messagebox.showinfo("Consulta", "Producto cargado en el formulario.")

    def actualizar(self):
        try:
            p = self.servicio.actualizar_producto(
                self.id_var.get(), self.nombre_var.get(),
                self.precio_var.get(), self.cantidad_var.get()
            )
            self._refrescar_tabla()
            messagebox.showinfo("Actualización", f"Producto '{p.nombre}' actualizado correctamente.")
        except ValueError as e:
            messagebox.showerror("Actualización", str(e))

    def eliminar(self):
        try:
            p = self.servicio.buscar_producto(self.id_var.get())
            if not p:
                raise ValueError("No se encontró un producto con ese ID.")
            if messagebox.askyesno("Confirmar", f"¿Desea eliminar '{p.nombre}'?"):
                self.servicio.eliminar_producto(self.id_var.get())
                self._refrescar_tabla()
                self.limpiar_formulario()
                messagebox.showinfo("Eliminación", "Producto eliminado correctamente.")
        except ValueError as e:
            messagebox.showerror("Eliminación", str(e))

    def limpiar_formulario(self):
        self.id_var.set("")
        self.nombre_var.set("")
        self.precio_var.set("")
        self.cantidad_var.set("")

    # ---------- Usuarios ----------
    def usuarios(self):
        """Gestión de usuarios (solo Administrador): formulario + Treeview + eventos."""
        self.estado.config(text="Sección activa: Usuarios")
        self._limpiar_contenido()

        if not self.servicio.es_administrador():
            self._mostrar_acceso_restringido()
            return

        self._titulo_seccion(
            "Gestión de usuarios",
            "Registre, consulte, actualice y elimine Empleados y Clientes del restaurante."
        )

        resumen = ttk.Frame(self.contenido)
        resumen.pack(fill="x", pady=(0, 10))
        self.tarjetas_usuarios = {
            "total": self._tarjeta_resumen(resumen, 0, "Usuarios registrados", 0),
            "admin": self._tarjeta_resumen(resumen, 1, "Administradores", 0),
            "empleado": self._tarjeta_resumen(resumen, 2, "Empleados", 0),
            "cliente": self._tarjeta_resumen(resumen, 3, "Clientes", 0),
        }

        self._construir_formulario_usuario()
        self._construir_tabla_usuarios()
        self._enlazar_eventos_usuarios()
        self._refrescar_usuarios()
        self.limpiar_formulario_usuario()

    def _mostrar_acceso_restringido(self):
        self._titulo_seccion(
            "Acceso restringido",
            "La gestión de usuarios está disponible solo para el rol Administrador."
        )
        ttk.Label(
            self.contenido,
            text="Su cuenta no tiene permiso para administrar usuarios.",
            image=self.icono_admin or "", compound="left", padding=10
        ).pack(anchor="w")

    def _construir_formulario_usuario(self):
        formulario = ttk.LabelFrame(self.contenido, text="Datos del usuario", padding=12)
        formulario.pack(fill="x", pady=(0, 8))

        self.u_id_var = tk.StringVar()
        self.u_nombre_var = tk.StringVar()
        self.u_usuario_var = tk.StringVar()
        self.u_contrasena_var = tk.StringVar()
        self.u_rol_var = tk.StringVar()

        etiquetas = ["ID", "Nombre completo", "Usuario", "Contraseña", "Rol"]
        for col, texto in enumerate(etiquetas):
            formulario.columnconfigure(col, weight=0 if col == 0 else 1)
            ttk.Label(formulario, text=texto).grid(row=0, column=col, sticky="w", padx=5)

        self.u_id_entry = ttk.Entry(
            formulario, textvariable=self.u_id_var, width=6, state="readonly"
        )
        self.u_nombre_entry = ttk.Entry(formulario, textvariable=self.u_nombre_var)
        self.u_usuario_entry = ttk.Entry(formulario, textvariable=self.u_usuario_var)
        self.u_contrasena_entry = ttk.Entry(
            formulario, textvariable=self.u_contrasena_var, show="*"
        )
        self.u_rol_combo = ttk.Combobox(
            formulario, textvariable=self.u_rol_var, state="readonly",
            values=self.servicio.listar_roles_gestionables()
        )
        for col, widget in enumerate([
            self.u_id_entry, self.u_nombre_entry, self.u_usuario_entry,
            self.u_contrasena_entry, self.u_rol_combo
        ]):
            widget.grid(row=1, column=col, sticky="ew", padx=5, pady=(4, 2))

        # Texto que reacciona a <<ComboboxSelected>>.
        self.u_rol_info = ttk.Label(formulario, text="", style="Info.TLabel")
        self.u_rol_info.grid(row=2, column=1, columnspan=4, sticky="w", padx=5, pady=(4, 0))
        ttk.Label(
            formulario,
            text="Al actualizar, deje la contraseña vacía para conservar la actual.",
            style="Hint.TLabel"
        ).grid(row=3, column=1, columnspan=4, sticky="w", padx=5)

        # Botones: se asocian con command= (clic del mouse).
        acciones = ttk.Frame(self.contenido)
        acciones.pack(fill="x", pady=(0, 8))
        self.u_botones = []
        for texto, icono, comando in [
            ("Registrar", self.icono_registrar, self.registrar_usuario),
            ("Actualizar", self.icono_actualizar, self.actualizar_usuario),
            ("Eliminar", self.icono_eliminar, self.eliminar_usuario),
            ("Limpiar", self.icono_limpiar, self.limpiar_formulario_usuario),
        ]:
            boton = ttk.Button(
                acciones, text=texto, image=icono, compound="left",
                command=comando,
                style="Danger.TButton" if texto == "Eliminar" else "Action.TButton"
            )
            boton.pack(side="left", padx=(0, 6))
            self.u_botones.append(boton)

        ttk.Label(
            acciones, text="Atajos: Enter = Registrar · Esc = Limpiar",
            style="Hint.TLabel"
        ).pack(side="right")

    def _construir_tabla_usuarios(self):
        contenedor = ttk.LabelFrame(self.contenido, text="Usuarios registrados", padding=8)
        contenedor.pack(fill="both", expand=True)
        # La contraseña no se muestra: la tabla solo contiene datos públicos.
        self.usuarios_tree = ttk.Treeview(
            contenedor, columns=("id", "nombre", "usuario", "rol"),
            show="headings", selectmode="browse", height=6
        )
        for c, h, w in [
            ("id", "ID", 80), ("nombre", "Nombre completo", 300),
            ("usuario", "Usuario", 220), ("rol", "Rol", 160)
        ]:
            self.usuarios_tree.heading(c, text=h)
            self.usuarios_tree.column(c, width=w, anchor="center")
        self.usuarios_tree.tag_configure(Usuario.ROL_ADMINISTRADOR, foreground=tema.ROJO)
        self.usuarios_tree.tag_configure(Usuario.ROL_EMPLEADO, foreground="#1F5F8B")
        self.usuarios_tree.tag_configure(Usuario.ROL_CLIENTE, foreground="#3E7A2E")
        scroll = ttk.Scrollbar(contenedor, orient="vertical", command=self.usuarios_tree.yview)
        self.usuarios_tree.configure(yscrollcommand=scroll.set)
        self.usuarios_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

    # ----- Eventos: bind() -----
    def _enlazar_eventos_usuarios(self):
        """Asocia los eventos de la sección con sus callbacks mediante bind()."""
        # Selección de una fila de la tabla -> cargar datos en el formulario.
        self.usuarios_tree.bind("<<TreeviewSelect>>", self._on_usuario_seleccionado)

        # Cambio de opción en el Combobox de rol.
        self.u_rol_combo.bind("<<ComboboxSelected>>", self._on_rol_seleccionado)

        # Enter desde los campos del formulario -> registrar.
        for widget in (self.u_nombre_entry, self.u_usuario_entry,
                       self.u_contrasena_entry, self.u_rol_combo):
            widget.bind("<Return>", self._on_return_registrar)

        # Escape desde cualquier control de la sección -> limpiar.
        for widget in (self.u_nombre_entry, self.u_usuario_entry,
                       self.u_contrasena_entry, self.u_rol_combo,
                       self.usuarios_tree, *self.u_botones):
            widget.bind("<Escape>", self._on_escape_limpiar)

    def _on_usuario_seleccionado(self, event):
        """<<TreeviewSelect>>: obtiene el ID de la fila y consulta al servicio."""
        seleccion = self.usuarios_tree.selection()
        if not seleccion:
            return  # También se dispara al limpiar la selección.
        id_usuario = self.usuarios_tree.item(seleccion[0], "values")[0]
        usuario = self.servicio.buscar_usuario(id_usuario)
        if not usuario:
            messagebox.showwarning("Consulta", "El usuario seleccionado ya no existe.")
            self._refrescar_usuarios()
            return
        self._cargar_usuario_en_formulario(usuario)

    def _on_rol_seleccionado(self, event):
        """<<ComboboxSelected>>: informa qué significa el rol elegido."""
        self._mostrar_info_rol(self.u_rol_var.get())

    def _on_return_registrar(self, event):
        """<Return>: atajo que reutiliza el mismo método del botón Registrar."""
        self.registrar_usuario()

    def _on_escape_limpiar(self, event):
        """<Escape>: atajo que reutiliza el mismo método del botón Limpiar."""
        self.limpiar_formulario_usuario()

    # ----- Operaciones (command= y atajos comparten estos métodos) -----
    def registrar_usuario(self):
        if self.u_id_var.get():
            messagebox.showwarning(
                "Registro",
                "Hay un usuario seleccionado. Use Actualizar para modificarlo "
                "o Limpiar (Esc) para registrar uno nuevo."
            )
            return
        try:
            nuevo = self.servicio.registrar_usuario(
                self.u_nombre_var.get(), self.u_usuario_var.get(),
                self.u_contrasena_var.get(), self.u_rol_var.get()
            )
        except (ValueError, PermissionError) as e:
            messagebox.showerror("Registro", str(e))
            return
        self._refrescar_usuarios()
        self.limpiar_formulario_usuario()
        messagebox.showinfo(
            "Registro", f"Usuario '{nuevo.usuario}' ({nuevo.rol}) registrado correctamente."
        )

    def actualizar_usuario(self):
        if not self.u_id_var.get():
            messagebox.showwarning("Actualización", "Seleccione un usuario de la tabla.")
            return
        try:
            usuario = self.servicio.actualizar_usuario(
                self.u_id_var.get(), self.u_nombre_var.get(), self.u_usuario_var.get(),
                self.u_contrasena_var.get(), self.u_rol_var.get()
            )
        except (ValueError, PermissionError) as e:
            messagebox.showerror("Actualización", str(e))
            return
        self._refrescar_usuarios(seleccionar=usuario.id)
        messagebox.showinfo(
            "Actualización", f"Usuario '{usuario.usuario}' actualizado correctamente."
        )

    def eliminar_usuario(self):
        if not self.u_id_var.get():
            messagebox.showwarning("Eliminación", "Seleccione un usuario de la tabla.")
            return
        try:
            usuario = self.servicio.validar_eliminacion_usuario(self.u_id_var.get())
            if not messagebox.askyesno(
                "Confirmar", f"¿Desea eliminar al usuario '{usuario.usuario}'?"
            ):
                return
            self.servicio.eliminar_usuario(usuario.id)
        except (ValueError, PermissionError) as e:
            messagebox.showerror("Eliminación", str(e))
            return
        self._refrescar_usuarios()
        self.limpiar_formulario_usuario()
        messagebox.showinfo("Eliminación", "Usuario eliminado correctamente.")

    def limpiar_formulario_usuario(self):
        """Devuelve la sección a su estado inicial y quita la selección de la tabla."""
        self.u_id_var.set("")
        self.u_nombre_var.set("")
        self.u_usuario_var.set("")
        self.u_contrasena_var.set("")
        self.u_rol_var.set(Usuario.ROL_CLIENTE)
        self._mostrar_info_rol(Usuario.ROL_CLIENTE)
        self.usuarios_tree.selection_remove(*self.usuarios_tree.selection())
        self.u_nombre_entry.focus_set()
        self.estado.config(text="Formulario de usuarios limpio")

    # ----- Apoyo de la vista -----
    def _cargar_usuario_en_formulario(self, usuario):
        self.u_id_var.set(str(usuario.id))
        self.u_nombre_var.set(usuario.nombre)
        self.u_usuario_var.set(usuario.usuario)
        self.u_contrasena_var.set("")  # La contraseña nunca se carga en la interfaz.
        self.u_rol_var.set(usuario.rol)
        self._mostrar_info_rol(usuario.rol)
        self.estado.config(text=f"Usuario seleccionado: {usuario.usuario}")

    def _mostrar_info_rol(self, rol):
        self.u_rol_info.config(
            text=f"{rol}: {self.servicio.descripcion_rol(rol)}" if rol else ""
        )
        if rol:
            self.estado.config(text=f"Rol seleccionado: {rol}")

    def _refrescar_usuarios(self, seleccionar=None):
        if not hasattr(self, "usuarios_tree") or not self.usuarios_tree.winfo_exists():
            return
        for item in self.usuarios_tree.get_children():
            self.usuarios_tree.delete(item)
        for u in self.servicio.listar_usuarios():
            self.usuarios_tree.insert(
                "", "end", iid=str(u.id), tags=(u.rol,),
                values=(u.id, u.nombre, u.usuario, u.rol)
            )
        total = len(self.servicio.listar_usuarios())
        self.tarjetas_usuarios["total"].valor.config(text=str(total))
        self.tarjetas_usuarios["admin"].valor.config(
            text=str(self.servicio.contar_por_rol(Usuario.ROL_ADMINISTRADOR)))
        self.tarjetas_usuarios["empleado"].valor.config(
            text=str(self.servicio.contar_por_rol(Usuario.ROL_EMPLEADO)))
        self.tarjetas_usuarios["cliente"].valor.config(
            text=str(self.servicio.contar_por_rol(Usuario.ROL_CLIENTE)))
        if seleccionar is not None and self.usuarios_tree.exists(str(seleccionar)):
            self.usuarios_tree.selection_set(str(seleccionar))

    # ---------- Ventas ----------
    def ventas(self):
        self.estado.config(text="Sección activa: Ventas")
        self._limpiar_contenido()
        self._titulo_seccion(
            "Registro de ventas",
            "Seleccione un usuario y un producto disponible para registrar la operación."
        )

        ventas = self.servicio.listar_ventas()
        productos = self.servicio.listar_productos()
        disponibles = sum(1 for p in productos if p.cantidad > 0)

        resumen = ttk.Frame(self.contenido)
        resumen.pack(fill="x", pady=(0, 10))
        self._tarjeta_resumen(resumen, 0, "Ventas registradas", len(ventas))
        self._tarjeta_resumen(resumen, 1, "Productos disponibles", disponibles)
        self._tarjeta_resumen(resumen, 2, "Usuarios", len(self.servicio.listar_usuarios()))

        formulario = ttk.LabelFrame(self.contenido, text="Nueva venta", padding=14)
        formulario.pack(fill="x", pady=(0, 10))
        formulario.columnconfigure(0, weight=1)
        formulario.columnconfigure(1, weight=1)

        self.usuario_var = tk.StringVar()
        self.producto_var = tk.StringVar()
        usuarios = self.servicio.listar_usuarios()
        productos = self.servicio.listar_productos()

        usuarios_opciones = [f"{u.id} - {u.nombre} ({u.usuario})" for u in usuarios]
        productos_opciones = [
            f"{p.id} - {p.nombre} | ${p.precio:.2f} | Stock: {p.cantidad}"
            for p in productos if p.cantidad > 0
        ]

        ttk.Label(formulario, text="Usuario").grid(row=0, column=0, sticky="w", padx=6)
        self.usuario_combo = ttk.Combobox(
            formulario, textvariable=self.usuario_var,
            values=usuarios_opciones, state="readonly"
        )
        self.usuario_combo.grid(row=1, column=0, sticky="ew", padx=6, pady=(4, 8))

        ttk.Label(formulario, text="Producto disponible").grid(row=0, column=1, sticky="w", padx=6)
        self.producto_combo = ttk.Combobox(
            formulario, textvariable=self.producto_var,
            values=productos_opciones, state="readonly"
        )
        self.producto_combo.grid(row=1, column=1, sticky="ew", padx=6, pady=(4, 8))

        ttk.Button(
            formulario, text="Registrar venta", command=self.registrar_venta,
            style="Primary.TButton"
        ).grid(row=2, column=0, columnspan=2, sticky="ew", padx=6, pady=(4, 2))

        ttk.Label(
            formulario,
            text="El botón inicia el callback, que solicita al servicio validar y registrar la operación."
        ).grid(row=3, column=0, columnspan=2, sticky="w", padx=6, pady=(4, 0))

        tabla_frame = ttk.LabelFrame(self.contenido, text="Historial de ventas", padding=8)
        tabla_frame.pack(fill="both", expand=True)
        self.ventas_tree = ttk.Treeview(
            tabla_frame, columns=("id", "usuario", "producto", "fecha"), show="headings"
        )
        for c, h, w in [
            ("id", "ID Venta", 90), ("usuario", "Usuario", 240),
            ("producto", "Producto", 320), ("fecha", "Fecha", 190)
        ]:
            self.ventas_tree.heading(c, text=h)
            self.ventas_tree.column(c, width=w, anchor="center")
        scroll = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.ventas_tree.yview)
        self.ventas_tree.configure(yscrollcommand=scroll.set)
        self.ventas_tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        self._refrescar_ventas()

    def registrar_venta(self):
        """Callback del botón Registrar venta."""
        if not self.usuario_var.get():
            messagebox.showwarning("Venta", "Seleccione un usuario antes de registrar la venta.")
            return
        if not self.producto_var.get():
            messagebox.showwarning("Venta", "Seleccione un producto antes de registrar la venta.")
            return

        try:
            usuario_id = int(self.usuario_var.get().split(" - ", 1)[0])
            producto_id = int(self.producto_var.get().split(" - ", 1)[0])
            venta = self.servicio.registrar_venta(usuario_id, producto_id)
            self._refrescar_ventas()
            self._actualizar_opciones_venta()

            usuario = self.servicio.buscar_usuario(venta.usuario_id)
            producto = self.servicio.buscar_producto(venta.producto_id)
            messagebox.showinfo(
                "Venta registrada",
                f"Venta #{venta.id} registrada correctamente.\n"
                f"Usuario: {usuario.nombre}\nProducto: {producto.nombre}\nFecha: {venta.fecha}"
            )
        except (ValueError, IndexError) as e:
            messagebox.showerror("Venta", str(e))

    def _refrescar_ventas(self):
        if not hasattr(self, "ventas_tree") or not self.ventas_tree.winfo_exists():
            return
        for item in self.ventas_tree.get_children():
            self.ventas_tree.delete(item)
        for venta in self.servicio.listar_ventas():
            usuario = self.servicio.buscar_usuario(venta.usuario_id)
            producto = self.servicio.buscar_producto(venta.producto_id)
            self.ventas_tree.insert(
                "", "end",
                values=(
                    venta.id,
                    usuario.nombre if usuario else "Usuario no encontrado",
                    producto.nombre if producto else "Producto no encontrado",
                    venta.fecha
                )
            )

    def _actualizar_opciones_venta(self):
        usuarios = self.servicio.listar_usuarios()
        productos = self.servicio.listar_productos()
        self.usuario_combo["values"] = [f"{u.id} - {u.nombre} ({u.usuario})" for u in usuarios]
        self.producto_combo["values"] = [
            f"{p.id} - {p.nombre} | ${p.precio:.2f} | Stock: {p.cantidad}"
            for p in productos if p.cantidad > 0
        ]
        self.usuario_var.set("")
        self.producto_var.set("")

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
        self._aplicar_permisos()
        self.productos()

    def ocultar(self):
        self.frame.pack_forget()
