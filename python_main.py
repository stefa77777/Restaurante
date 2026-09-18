import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

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
        self.costo_total = float(self.numero_sesiones) * float(self.costo_sesion)
        return self.costo_total


class VentanaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Acceso al Sistema - Gestión de Clientes")
        self.root.geometry("450x320")
        self.root.resizable(False, False)
        
        # Centrar la ventana en la pantalla
        self.root.eval('tk::PlaceWindow . center')

        # Encabezado: Nombre de la Aplicación y Autor
        lbl_titulo_app = tk.Label(root, text="SISTEMA DE GESTIÓN DE CLIENTES", 
                                  font=("Arial", 14, "bold"), fg="#1a237e")
        lbl_titulo_app.pack(pady=(20, 5))

        lbl_autor = tk.Label(root, text="Desarrollado por: Andrea Redondo", 
                             font=("Arial", 10, "italic"), fg="#424242")
        lbl_autor.pack(pady=(0, 20))

        #Autenticación
        frame_login = tk.LabelFrame(root, text=" Autenticación de Seguridad ", 
                                    font=("Arial", 10, "bold"), padx=15, pady=15)
        frame_login.pack(padx=30, pady=10, fill="both")

        lbl_pass = tk.Label(frame_login, text="Ingrese la Contraseña:", font=("Arial", 10))
        lbl_pass.pack(pady=5)

        self.txt_pass = tk.Entry(frame_login, show="*", font=("Arial", 11), width=20, justify="center")
        self.txt_pass.pack(pady=5)
        self.txt_pass.focus()

        
        self.txt_pass.bind("<Return>", lambda event: self.validar_acceso())

        
        btn_ingresar = tk.Button(frame_login, text="Ingresar al Sistema", bg="#1976d2", fg="white", 
                                 font=("Arial", 10, "bold"), command=self.validar_acceso)
        btn_ingresar.pack(pady=10)

    def validar_acceso(self):
        clave_ingresada = self.txt_pass.get()
        CLAVE_CORRECTA = "1793"

        if clave_ingresada == CLAVE_CORRECTA:
            messagebox.showinfo("Acceso Concedido", "Bienvenida/o al Sistema de Gestión de Clientes.")
            self.root.destroy()  # Cierra la ventana de Login
            abrir_ventana_principal()  # Abre la aplicación principal
        else:
            messagebox.showerror("Error de Autenticación", "Contraseña incorrecta. Intente nuevamente.")
            self.txt_pass.delete(0, tk.END)



class AppGestionClientes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Clientes - Andrea Redondo")
        self.root.geometry("820x600")
        self.root.resizable(False, False)

        # Encabezado principal
        lbl_titulo = tk.Label(root, text="Registro de Clientes y Cálculo de Costo", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=10)

        # Formulario de datos
        frame_form = tk.LabelFrame(root, text=" Datos del Cliente ", font=("Arial", 11, "bold"), padx=15, pady=10)
        frame_form.pack(fill="x", padx=20, pady=5)

        tk.Label(frame_form, text="Identificación:").grid(row=0, column=0, sticky="e", pady=5, padx=5)
        self.txt_identificacion = tk.Entry(frame_form, width=25)
        self.txt_identificacion.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Nombre Completo:").grid(row=0, column=2, sticky="e", pady=5, padx=5)
        self.txt_nombre = tk.Entry(frame_form, width=25)
        self.txt_nombre.grid(row=0, column=3, pady=5, padx=5)

        tk.Label(frame_form, text="Género:").grid(row=1, column=0, sticky="e", pady=5, padx=5)
        self.cmb_genero = ttk.Combobox(frame_form, values=["Femenino", "Masculino", "Otro"], state="readonly", width=22)
        self.cmb_genero.current(0)
        self.cmb_genero.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Tipo de Menú:").grid(row=1, column=2, sticky="e", pady=5, padx=5)
        self.cmb_menu = ttk.Combobox(frame_form, values=["Estándar", "Vegetariano", "Vegano", "Especial"], state="readonly", width=22)
        self.cmb_menu.current(0)
        self.cmb_menu.grid(row=1, column=3, pady=5, padx=5)

        tk.Label(frame_form, text="Número de Sesiones:").grid(row=2, column=0, sticky="e", pady=5, padx=5)
        self.txt_sesiones = tk.Entry(frame_form, width=25)
        self.txt_sesiones.grid(row=2, column=1, pady=5, padx=5)

        tk.Label(frame_form, text="Costo por Sesión ($):").grid(row=2, column=2, sticky="e", pady=5, padx=5)
        self.txt_costo = tk.Entry(frame_form, width=25)
        self.txt_costo.grid(row=2, column=3, pady=5, padx=5)

        btn_calcular = tk.Button(root, text="Calcular Costo Total y Registrar", bg="#2e7d32", fg="white", 
                                 font=("Arial", 11, "bold"), command=self.procesar_registro)
        btn_calcular.pack(pady=10)

        # Tabla de Registros
        frame_tabla = tk.LabelFrame(root, text=" Clientes Registrados ", font=("Arial", 11, "bold"), padx=10, pady=10)
        frame_tabla.pack(fill="both", expand=True, padx=20, pady=5)

        columnas = ("ID", "Nombre", "Género", "Menú", "Sesiones", "Costo/S", "Total", "Fecha")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)

        anchos = {"ID": 80, "Nombre": 140, "Género": 80, "Menú": 90, "Sesiones": 65, "Costo/S": 75, "Total": 85, "Fecha": 130}
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=anchos[col], anchor="center")

        self.tabla.pack(fill="both", expand=True)

    def procesar_registro(self):
        try:
            identificacion = self.txt_identificacion.get().strip()
            nombre = self.txt_nombre.get().strip()
            genero = self.cmb_genero.get()
            tipo_menu = self.cmb_menu.get()
            num_sesiones = int(self.txt_sesiones.get().strip())
            costo_sesion = float(self.txt_costo.get().strip())
            fecha_actual = datetime.now()

            if not identificacion or not nombre:
                messagebox.showwarning("Atención", "Por favor complete los campos obligatorios.")
                return

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

            self.tabla.insert("", "end", values=(
                cliente.identificacion,
                cliente.nombre_completo,
                cliente.genero,
                cliente.tipo_menu,
                cliente.numero_sesiones,
                f"${cliente.costo_sesion:.2f}",
                f"${costo_total:.2f}",
                cliente.fecha_registro.strftime("%Y-%m-%d %H:%M")
            ))

            self.limpiar_formulario()

        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos para sesiones y costo.")

    def limpiar_formulario(self):
        self.txt_identificacion.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_sesiones.delete(0, tk.END)
        self.txt_costo.delete(0, tk.END)
        self.cmb_genero.current(0)
        self.cmb_menu.current(0)


def abrir_ventana_principal():
    root_principal = tk.Tk()
    app = AppGestionClientes(root_principal)
    root_principal.mainloop()


if __name__ == "__main__":
    root_login = tk.Tk()
    login_app = VentanaLogin(root_login)
    root_login.mainloop()