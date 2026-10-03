import tkinter as tk
from tkinter import messagebox

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView
from ui.tema import aplicar_tema


class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Restaurante App - Semana 16")
        self.root.geometry("1080x700")
        self.root.minsize(900, 600)
        aplicar_tema(root)

        try:
            self.servicio = RestauranteServicio(ArchivoServicio())
            servicio = self.servicio
            self.login = LoginView(root, servicio, self.mostrar_principal)
            self.principal = MainView(root, servicio, self.cerrar_sesion)
            self.principal.ocultar()
            self.login.mostrar()
        except Exception as e:
            messagebox.showerror("Error", str(e))
            root.destroy()

    def mostrar_principal(self):
        self.login.ocultar()
        self.principal.mostrar()

    def cerrar_sesion(self):
        self.servicio.cerrar_sesion()
        self.principal.ocultar()
        self.login.limpiar()
        self.login.mostrar()


if __name__ == "__main__":
    root = tk.Tk()
    RestauranteApp(root)
    root.mainloop()
