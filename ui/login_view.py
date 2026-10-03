import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from ui import tema
from ui.tema import aplicar_tema


class LoginView:
    def __init__(self, root, servicio, on_login):
        self.root, self.servicio, self.on_login = root, servicio, on_login
        aplicar_tema(root)
        self.frame = ttk.Frame(root, padding=35)

        # Tarjeta centrada "Acceso al sistema".
        tarjeta = ttk.LabelFrame(self.frame, text="Acceso al sistema", padding=(30, 22))
        tarjeta.pack(expand=True)

        logo_path = Path(__file__).resolve().parent.parent / "assets" / "logo_restaurante.png"
        try:
            self.logo = tk.PhotoImage(file=str(logo_path))
            ttk.Label(tarjeta, image=self.logo).pack(pady=(0, 14))
        except tk.TclError:
            self.logo = None

        ttk.Label(
            tarjeta, text="RESTAURANTE APP",
            font=(tema.FUENTE, 20, "bold"), foreground=tema.TEXTO
        ).pack()
        ttk.Label(tarjeta, text="Inicio de sesión").pack(pady=(8, 4))

        form = ttk.Frame(tarjeta)
        form.pack(pady=15)

        ttk.Label(form, text="Usuario:").grid(row=0, column=0, padx=6, pady=7, sticky="e")
        self.usuario = tk.StringVar()
        entrada_usuario = ttk.Entry(form, textvariable=self.usuario, width=26)
        entrada_usuario.grid(row=0, column=1, padx=6, pady=7)

        ttk.Label(form, text="Contraseña:").grid(row=1, column=0, padx=6, pady=7, sticky="e")
        self.contrasena = tk.StringVar()
        entrada_contrasena = ttk.Entry(
            form, textvariable=self.contrasena, show="*", width=26
        )
        entrada_contrasena.grid(row=1, column=1, padx=6, pady=7)

        # Atajo de teclado: Enter en cualquiera de los campos reutiliza ingresar().
        for entrada in (entrada_usuario, entrada_contrasena):
            entrada.bind("<Return>", self._on_return_ingresar)
        self.entrada_usuario = entrada_usuario

        ttk.Button(
            tarjeta, text="Ingresar", command=self.ingresar, style="Primary.TButton"
        ).pack(fill="x", pady=(6, 10))

        ttk.Label(
            tarjeta, text="Acceso de prueba: admin / 1234",
            style="Hint.TLabel"
        ).pack()
        ttk.Label(
            tarjeta, text="Empleado: mesero / 1234  ·  Cliente: cliente / 1234",
            style="Hint.TLabel"
        ).pack()

    def ingresar(self):
        u, p = self.usuario.get().strip(), self.contrasena.get()

        if not u or not p:
            messagebox.showwarning(
                "Acceso", "Ingrese usuario y contraseña."
            )
        elif self.servicio.iniciar_sesion(u, p):
            self.on_login()
        else:
            messagebox.showerror(
                "Acceso", "Usuario o contraseña incorrectos."
            )

    def _on_return_ingresar(self, event):
        """Callback de <Return>: reutiliza el método del botón Ingresar."""
        self.ingresar()

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
        self.entrada_usuario.focus_set()

    def ocultar(self):
        self.frame.pack_forget()

    def limpiar(self):
        self.usuario.set("")
        self.contrasena.set("")
