"""Tema visual compartido por LoginView y MainView (paleta del logo del restaurante)."""
import tkinter as tk
from tkinter import ttk

FUENTE = "Segoe UI"

FONDO = "#F4ECE2"        # crema de fondo
TARJETA = "#FFFFFF"      # encabezado y campos
CREMA = "#FDF5E6"        # botones de navegación
NAVEGACION = "#EAD9C6"   # barra de menú
NARANJA = "#D35400"      # color principal
NARANJA_OSCURO = "#B34700"
NARANJA_CLARO = "#F6D3B3"  # fila seleccionada
ROJO = "#8B2A1A"         # títulos y bordes
LADRILLO = "#B03A2E"     # acción de eliminar
TEXTO = "#3C281E"
TEXTO_SUAVE = "#7A6A5F"
BORDE = "#D9B99B"


def aplicar_tema(root):
    """Configura los estilos ttk de toda la aplicación (es seguro llamarla varias veces)."""
    root.configure(background=FONDO)
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(".", background=FONDO, foreground=TEXTO, font=(FUENTE, 9))
    style.configure("TFrame", background=FONDO)
    style.configure("App.TFrame", background=FONDO, padding=0)
    style.configure("Content.TFrame", background=FONDO)
    style.configure("Header.TFrame", background=TARJETA)
    style.configure("Nav.TFrame", background=NAVEGACION)

    style.configure("TLabel", background=FONDO, foreground=TEXTO, font=(FUENTE, 9))
    style.configure("Header.TLabel", background=TARJETA)
    style.configure("Nav.TLabel", background=NAVEGACION, font=(FUENTE, 9, "bold"))
    style.configure("Title.TLabel", font=(FUENTE, 18, "bold"), foreground=TEXTO)
    style.configure("Subtitle.TLabel", font=(FUENTE, 9), foreground=TEXTO_SUAVE)
    style.configure("Section.TLabel", font=(FUENTE, 15, "bold"), foreground=ROJO)
    style.configure("CardTitle.TLabel", font=(FUENTE, 9, "bold"))
    style.configure("CardValue.TLabel", font=(FUENTE, 16, "bold"), foreground=NARANJA)
    style.configure("Hint.TLabel", font=(FUENTE, 9, "italic"), foreground=TEXTO_SUAVE)
    style.configure("Info.TLabel", font=(FUENTE, 9, "bold"), foreground=ROJO)

    style.configure("TLabelframe", background=FONDO, bordercolor=NARANJA, relief="solid")
    style.configure("TLabelframe.Label", background=FONDO, foreground=ROJO,
                    font=(FUENTE, 9, "bold"))

    # Botones: naranja de acción, crema de navegación y ladrillo para eliminar.
    style.configure("TButton", background=NARANJA, foreground="#FFFFFF",
                    font=(FUENTE, 9, "bold"), borderwidth=0, focusthickness=0,
                    padding=(10, 7))
    style.map("TButton",
              background=[("pressed", NARANJA_OSCURO), ("active", NARANJA_OSCURO)])
    style.configure("Action.TButton", font=(FUENTE, 9, "bold"), padding=(10, 7))
    style.configure("Primary.TButton", font=(FUENTE, 10, "bold"), padding=(14, 8))
    style.configure("Danger.TButton", background=LADRILLO, padding=(10, 7))
    style.map("Danger.TButton",
              background=[("pressed", ROJO), ("active", ROJO)])
    style.configure("Nav.TButton", background=CREMA, foreground=TEXTO,
                    font=(FUENTE, 10, "bold"), padding=(12, 9))
    style.map("Nav.TButton",
              background=[("pressed", NARANJA), ("active", NARANJA_CLARO)],
              foreground=[("pressed", "#FFFFFF")])

    style.configure("TEntry", padding=6, fieldbackground=TARJETA, bordercolor=BORDE,
                    lightcolor=BORDE, darkcolor=BORDE)
    style.map("TEntry", bordercolor=[("focus", NARANJA)], lightcolor=[("focus", NARANJA)])
    style.configure("TCombobox", padding=5, fieldbackground=TARJETA, background=CREMA,
                    bordercolor=BORDE, arrowcolor=ROJO)
    style.map("TCombobox", fieldbackground=[("readonly", TARJETA)],
              bordercolor=[("focus", NARANJA)])
    root.option_add("*TCombobox*Listbox.background", TARJETA)
    root.option_add("*TCombobox*Listbox.selectBackground", NARANJA)

    style.configure("Treeview", rowheight=30, font=(FUENTE, 9), background=TARJETA,
                    fieldbackground=TARJETA, foreground=TEXTO, bordercolor=BORDE)
    style.map("Treeview", background=[("selected", NARANJA_CLARO)],
              foreground=[("selected", TEXTO)])
    style.configure("Treeview.Heading", font=(FUENTE, 9, "bold"), background=NARANJA,
                    foreground="#FFFFFF", relief="flat", padding=(4, 6))
    style.map("Treeview.Heading", background=[("active", NARANJA_OSCURO)])
    style.configure("Vertical.TScrollbar", background=BORDE, troughcolor=FONDO,
                    arrowcolor=ROJO)
