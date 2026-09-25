import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re

COLOR_FONDO = "#E0F2FE"
COLOR_CONTAINER = "#BAE6FD"
COLOR_PRIMARIO = "#38BDF8"
COLOR_BOTON_REGISTRAR = "#0284C7"
COLOR_BOTON_SALIR = "#DC2626"
COLOR_BOTON_VACIAR = "#E11D48"
COLOR_TEXTO = "#000000"

PRECIOS_MENU = {
    "Ejecutivo": 35000.0,
    "Vegetariano": 28000.0,
    "Degustación": 75000.0,
    "Infantil": 20000.0,
    "Gourmet": 95000.0
}


class GestionClientes:
    def __init__(self, identificacion: str, nombre_completo: str, genero: str, 
                 tipo_menu: str, numero_sesiones: int, fecha_registro: datetime, costo_sesion: float):
        self.identificacion: str = identificacion
        self.nombre_completo: str = nombre_completo
        self.genero: str = genero
        self.tipo_menu: str = tipo_menu
        self.numero_sesiones: int = numero_sesiones
        self.fecha_registro: datetime = fecha_registro
        self.costo_sesion: float = costo_sesion
        self.costo_total: float = 0.0

    def calcular_costo_total(self) -> float:
        """Fórmula: costo_total = numero_sesiones * costo_sesion"""
        self.costo_total = float(self.numero_sesiones) * float(self.costo_sesion)
        return self.costo_total

class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Acceso al Sistema - Gestión de Clientes")
        self.root.geometry("460x320")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_FONDO)
        self.root.eval('tk::PlaceWindow . center')

        # Encabezado
        lbl_titulo_app = tk.Label(root, text="SISTEMA DE GESTIÓN DE CLIENTES", 
                                  font=("Arial", 14, "bold"), fg=COLOR_PRIMARIO, bg=COLOR_FONDO)
        lbl_titulo_app.pack(pady=(20, 5))

        lbl_autor = tk.Label(root, text="Desarrollado por: Andrea Redondo", 
                             font=("Arial", 10, "italic"), fg="#4B5563", bg=COLOR_FONDO)
        lbl_autor.pack(pady=(0, 15))

        # Panel de Autenticación
        frame_login = tk.LabelFrame(root, text=" Autenticación de Seguridad ", 
                                    font=("Arial", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO, padx=15, pady=15)
        frame_login.pack(padx=30, pady=10, fill="both")

        lbl_pass = tk.Label(frame_login, text="Ingrese la Contraseña:", font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO)
        lbl_pass.pack(pady=5)

        # Enmascarado de clave
        self.txt_pass = tk.Entry(frame_login, show="*", font=("Arial", 11), width=20, justify="center")
        self.txt_pass.pack(pady=5)
        self.txt_pass.focus()
        self.txt_pass.bind("<Return>", lambda event: self.validar_acceso())

        btn_ingresar = tk.Button(frame_login, text="Ingresar al Sistema", bg=COLOR_PRIMARIO, fg="white", 
                                 font=("Arial", 10, "bold"), command=self.validar_acceso, cursor="hand2")
        btn_ingresar.pack(pady=10)

    def validar_acceso(self):
        if self.txt_pass.get() == "1793":
            messagebox.showinfo("Acceso Concedido", "Bienvenida/o al Sistema de Gestión de Clientes.")
            self.root.destroy()
            abrir_ventana_principal()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta. Intente nuevamente.")
            self.txt_pass.delete(0, tk.END)

class VentanaReporte(tk.Toplevel):
    def __init__(self, parent, cliente: GestionClientes):
        super().__init__(parent.root)
        self.parent = parent
        self.cliente = cliente

        self.title("Reporte General del Cliente")
        self.geometry("450x420")
        self.resizable(False, False)
        self.configure(bg=COLOR_FONDO)
        self.grab_set()  # Ventana modal (bloquea la de atrás hasta cerrar)

        lbl_titulo = tk.Label(self, text="REPORTE DE REGISTRO Y LIQUIDACIÓN", 
                              font=("Arial", 12, "bold"), fg=COLOR_PRIMARIO, bg=COLOR_FONDO)
        lbl_titulo.pack(pady=15)

        frame_info = tk.LabelFrame(self, text=" Resumen del Cliente ", font=("Arial", 10, "bold"), 
                                   bg=COLOR_FONDO, fg=COLOR_TEXTO, padx=15, pady=15)
        frame_info.pack(padx=20, pady=5, fill="both", expand=True)

        datos = [
            ("Identificación:", cliente.identificacion),
            ("Nombre Completo:", cliente.nombre_completo),
            ("Género:", cliente.genero),
            ("Tipo de Menú:", cliente.tipo_menu),
            ("Costo por Sesión:", f"${cliente.costo_sesion:,.0f}"),
            ("Número de Sesiones:", str(cliente.numero_sesiones)),
            ("Fecha de Registro:", cliente.fecha_registro.strftime("%Y-%m-%d %H:%M")),
            ("COSTO TOTAL A PAGAR:", f"${cliente.costo_total:,.0f}")
        ]

        for i, (label, valor) in enumerate(datos):
            es_total = (label == "COSTO TOTAL A PAGAR:")
            font_style = ("Arial", 10, "bold") if es_total else ("Arial", 10)
            color_txt = COLOR_PRIMARIO if es_total else COLOR_TEXTO

            lbl_lbl = tk.Label(frame_info, text=label, font=font_style, bg=COLOR_FONDO, fg=color_txt, anchor="w")
            lbl_lbl.grid(row=i, column=0, sticky="w", pady=3)

            lbl_val = tk.Label(frame_info, text=valor, font=font_style, bg=COLOR_FONDO, fg=color_txt, anchor="e")
            lbl_val.grid(row=i, column=1, sticky="e", pady=3, padx=10)

        frame_info.columnconfigure(1, weight=1)

        btn_cerrar = tk.Button(self, text="Cerrar y Limpiar Formulario", bg=COLOR_PRIMARIO, fg="white", 
                               font=("Arial", 10, "bold"), command=self.cerrar_reporte, cursor="hand2")
        btn_cerrar.pack(pady=15)

        self.protocol("WM_DELETE_WINDOW", self.cerrar_reporte)

    def cerrar_reporte(self):
        self.grab_release()
        self.destroy()
        self.parent.limpiar_formulario()


class AppGestionClientes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Clientes - Andrea Redondo")
        self.root.geometry("850x670")
        self.root.resizable(False, False)
        self.root.configure(bg=COLOR_FONDO)

        # Confirmación de salida al cerrar la ventana desde la 'X'
        self.root.protocol("WM_DELETE_WINDOW", self.confirmar_salida)

        # Encabezado principal
        lbl_titulo = tk.Label(root, text="Registro de Clientes y Cálculo de Costo", 
                              font=("Arial", 16, "bold"), fg=COLOR_PRIMARIO, bg=COLOR_FONDO)
        lbl_titulo.pack(pady=10)

        # Formulario
        frame_form = tk.LabelFrame(root, text=" Datos del Cliente ", font=("Arial", 11, "bold"), 
                                   bg=COLOR_FONDO, fg=COLOR_TEXTO, padx=15, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        # Fila 0
        tk.Label(frame_form, text="Identificación (Números):", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.txt_identificacion = tk.Entry(frame_form, width=25)
        self.txt_identificacion.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Nombre Completo (Letras):", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=2, sticky="e", pady=5, padx=5)
        self.txt_nombre = tk.Entry(frame_form, width=25)
        self.txt_nombre.grid(row=0, column=3, pady=5, padx=5)

        # Fila 1
        tk.Label(frame_form, text="Género:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.cmb_genero = ttk.Combobox(frame_form, values=["Femenino", "Masculino", "Otro"], state="readonly", width=22)
        self.cmb_genero.current(0)
        self.cmb_genero.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Tipo de Menú:", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=1, column=2, sticky="e", pady=5, padx=5)
        self.cmb_menu = ttk.Combobox(frame_form, values=list(PRECIOS_MENU.keys()), state="readonly", width=22)
        self.cmb_menu.current(0)
        self.cmb_menu.grid(row=1, column=3, pady=5, padx=5)
        self.cmb_menu.bind("<<ComboboxSelected>>", self.actualizar_costo_automatico)

        # Fila 2
        tk.Label(frame_form, text="Número de Sesiones (>0):", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.txt_sesiones = tk.Entry(frame_form, width=25)
        self.txt_sesiones.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Costo por Sesión ($):", bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=2, column=2, sticky="e", pady=5, padx=5)
        self.txt_costo = tk.Entry(frame_form, width=25, state="readonly")
        self.txt_costo.grid(row=2, column=3, pady=5, padx=5)

        # Actualizar el valor inicial del costo
        self.actualizar_costo_automatico()

        # Botones de Acción
        frame_botones = tk.Frame(root, bg=COLOR_FONDO)
        frame_botones.pack(pady=10)

        btn_calcular = tk.Button(frame_botones, text="Calcular Costo Total y Registrar", bg=COLOR_BOTON_REGISTRAR, fg="white", 
                                 font=("Arial", 11, "bold"), command=self.procesar_registro, cursor="hand2", padx=10)
        btn_calcular.pack(side="left", padx=10)

        btn_salir = tk.Button(frame_botones, text="Salir", bg=COLOR_BOTON_SALIR, fg="white", 
                              font=("Arial", 11, "bold"), command=self.confirmar_salida, cursor="hand2", padx=15)
        btn_salir.pack(side="left", padx=10)

        # Tabla de Registros
        frame_tabla = tk.LabelFrame(root, text=" Clientes Registrados ", font=("Arial", 11, "bold"), 
                                    bg=COLOR_FONDO, fg=COLOR_TEXTO, padx=10, pady=10)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=5)

        columnas = ("ID", "Nombre", "Género", "Menú", "Sesiones", "Costo/S", "Total", "Fecha")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=7)

        anchos = {"ID": 80, "Nombre": 140, "Género": 80, "Menú": 90, "Sesiones": 65, "Costo/S": 85, "Total": 95, "Fecha": 120}
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=anchos[col], anchor="center")

        self.tabla.pack(fill="both", expand=True)

        # Botón para limpiar de forma explícita la lista de clientes registrados
        btn_limpiar_tabla = tk.Button(frame_tabla, text="Limpiar Registro de Clientes Registrados", bg=COLOR_BOTON_VACIAR, fg="white", 
                                      font=("Arial", 10, "bold"), command=self.limpiar_tabla_clientes, cursor="hand2")
        btn_limpiar_tabla.pack(pady=(10, 0))

    def actualizar_costo_automatico(self, event=None):
        """Asigna el valor por sesión automáticamente según el menú seleccionado."""
        menu_seleccionado = self.cmb_menu.get()
        costo = PRECIOS_MENU.get(menu_seleccionado, 0.0)
        
        self.txt_costo.config(state="normal")
        self.txt_costo.delete(0, tk.END)
        self.txt_costo.insert(0, f"${costo:,.0f}")
        self.txt_costo.config(state="readonly")

    def validar_datos(self) -> bool:
        """Aplica las reglas de validación de los requerimientos."""
        identificacion = self.txt_identificacion.get().strip()
        nombre = self.txt_nombre.get().strip()
        sesiones_str = self.txt_sesiones.get().strip()

        # 1. Validación Identificación (Solo números)
        if not identificacion.isdigit():
            messagebox.showerror("Error en Identificación", "La identificación debe contener únicamente dígitos numéricos.")
            return False

        # 2. Validación Nombre (Solo letras y espacios)
        if not re.match(r"^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre):
            messagebox.showerror("Error en Nombre", "El nombre completo debe contener únicamente letras y espacios.")
            return False

        # 3. Validación Sesiones (Entero mayor que 0)
        try:
            sesiones = int(sesiones_str)
            if sesiones <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error en Sesiones", "El número de sesiones debe ser un entero mayor que cero (1, 2, 3...).")
            return False

        return True

    def procesar_registro(self):
        if not self.validar_datos():
            return

        identificacion = self.txt_identificacion.get().strip()
        nombre = self.txt_nombre.get().strip()
        genero = self.cmb_genero.get()
        tipo_menu = self.cmb_menu.get()
        num_sesiones = int(self.txt_sesiones.get().strip())
        costo_sesion = PRECIOS_MENU[tipo_menu]
        fecha_actual = datetime.now()

        # Instanciar clase de la tabla de abstracción
        cliente = GestionClientes(
            identificacion=identificacion,
            nombre_completo=nombre,
            genero=genero,
            tipo_menu=tipo_menu,
            numero_sesiones=num_sesiones,
            fecha_registro=fecha_actual,
            costo_sesion=costo_sesion
        )

        costo_total = cliente.calcular_costo_total()

        # Insertar registro en la tabla visual
        self.tabla.insert("", "end", values=(
            cliente.identificacion,
            cliente.nombre_completo,
            cliente.genero,
            cliente.tipo_menu,
            cliente.numero_sesiones,
            f"${cliente.costo_sesion:,.0f}",
            f"${costo_total:,.0f}",
            cliente.fecha_registro.strftime("%Y-%m-%d %H:%M")
        ))

        # Abrir Ventana de Reporte
        VentanaReporte(self, cliente) 

    def limpiar_formulario(self):
        """Limpia únicamente los campos de entrada del formulario."""
        self.txt_identificacion.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_sesiones.delete(0, tk.END)
        self.cmb_genero.current(0)
        self.cmb_menu.current(0)
        self.actualizar_costo_automatico()
        self.txt_identificacion.focus()

    def limpiar_tabla_clientes(self):
        """Vacía por completo el historial de clientes registrados en la tabla."""
        if self.tabla.get_children():
            confirmacion = messagebox.askyesno("Confirmar Limpieza", "¿Desea eliminar todos los clientes de la lista visual?")
            if confirmacion:
                for item in self.tabla.get_children():
                    self.tabla.delete(item)

    def confirmar_salida(self):
        """Muestra ventana de confirmación antes de cerrar la aplicación."""
        respuesta = messagebox.askyesno("Confirmar Salida", "¿Está seguro que desea salir de la aplicación?")
        if respuesta:
            self.root.destroy()


def abrir_ventana_principal():
    root_principal = tk.Tk()
    app = AppGestionClientes(root_principal)
    root_principal.mainloop()

if __name__ == "__main__":
    root_login = tk.Tk()
    login_app = VentanaLogin(root_login)
    root_login.mainloop()