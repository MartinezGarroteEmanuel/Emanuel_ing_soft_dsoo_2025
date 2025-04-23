import tkinter as tk
from tkinter import ttk
import sqlite3
import datetime  # fechas y horas
import tkinter.messagebox as messagebox #cuadro de mensaje

"esto es una prueba"
def cerrar_ventana_medico():
    ventana_cargar_medico.destroy()

def cerrar_ventana_paciente():
    ventana_cargar_paciente.destroy()

def conectar_db():
    conn = sqlite3.connect(r"C:/Users/marti/Desktop/sq/Hospital.db")  # Ruta 
    return conn


def mostrar_informe_camas_ocupadas():
    ventana_informe = tk.Toplevel(ventana)
    ventana_informe.title("Informe de Camas Ocupadas")


    tree = ttk.Treeview(ventana_informe, columns=("Codigo Ingreso", "Habitacion", "Cama", "Codigo Paciente", "Codigo Medico"), show="headings")
    #tabla visual
    tree.heading("Codigo Ingreso", text="Código Ingreso") #establece los encabezados de las columnas
    tree.heading("Habitacion", text="Habitación")
    tree.heading("Cama", text="Cama")
    tree.heading("Codigo Paciente", text="Código Paciente")
    tree.heading("Codigo Medico", text="Código Médico")
    
    tree.grid(row=0, column=0, padx=10, pady=10)

    # Obtener los datos de ingresos
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, habitacion, cama, codigo_paciente, codigo_medico FROM Ingresos")
    ingresos = cursor.fetchall()
    conn.close()

    for ingreso in ingresos:
        tree.insert("", tk.END, values=ingreso)

    ttk.Button(ventana_informe, text="Cerrar", command=ventana_informe.destroy).grid(row=1, column=0, padx=10, pady=10)

# Función para guardar un médico en la base de datos
def guardar_medico():
    codigo = entry_codigo.get()
    apellido = entry_apellido.get()
    nombre = entry_nombre.get()
    matricula = entry_matricula.get()
    especialidad = entry_especialidad.get()

    conn = conectar_db() #establece conexion
    cursor = conn.cursor()#consultas SQL sobre la base de datos.

    try:
        cursor.execute("""
            INSERT INTO Medicos (codigo, apellido, nombre, matricula, especialidad)
            VALUES (?, ?, ?, ?, ?)
        """, (codigo, apellido, nombre, matricula, especialidad))
        conn.commit() # guarda los cambios en la base de datos.

        print("Médico guardado correctamente")
    except sqlite3.IntegrityError:
        print("Error: El código del médico ya existe.")
    
    conn.close()

    entry_codigo.delete(0, tk.END) #limpia campos de entrada
    entry_apellido.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_matricula.delete(0, tk.END)
    entry_especialidad.delete(0, tk.END)

# Función para guardar un paciente en la base de datos
def guardar_paciente():
    codigo = entry_codigo.get()
    apellido = entry_apellido.get()
    nombre = entry_nombre.get()
    obra_social = entry_obra_social.get()
    num_obra_social = entry_nro_obra_social.get()
    domicilio = entry_domicilio.get()
    telefono = entry_telefono.get()

    conn = conectar_db()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO Pacientes (codigo, apellido, nombre, obra_social, num_obra_social, domicilio, telefono)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (codigo, apellido, nombre, obra_social, num_obra_social, domicilio, telefono))
        conn.commit() #guarda en base de datos
        print("Paciente guardado correctamente")
    except sqlite3.IntegrityError:
        print("Error: El código del paciente ya existe.")
    
    conn.close()

    entry_codigo.delete(0, tk.END)
    entry_apellido.delete(0, tk.END)
    entry_nombre.delete(0, tk.END)
    entry_obra_social.delete(0, tk.END)
    entry_nro_obra_social.delete(0, tk.END)
    entry_domicilio.delete(0, tk.END)
    entry_telefono.delete(0, tk.END)

# Función para guardar un ingreso
def guardar_ingreso(codigo_ingreso, habitacion, cama, fecha_ingreso, codigo_paciente, codigo_medico):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Pacientes WHERE codigo=?", (codigo_paciente,)) 
    # verifica si el paciente con el codigo_paciente proporcionado existe en la tabla Pacientes, si no retorna 0
    if cursor.fetchone()[0] == 0:
        print("Error: El código de paciente no existe.")
        conn.close()
        return

    cursor.execute("SELECT COUNT(*) FROM Medicos WHERE codigo=?", (codigo_medico,))
    if cursor.fetchone()[0] == 0:
        print("Error: El código de médico no existe.")
        conn.close()
        return

    # Si no se proporciona un código de ingreso, se genera automáticamente
    if not codigo_ingreso:
        codigo_ingreso = f"{codigo_paciente}_{fecha_ingreso}" 

    try:
        #insertar
        cursor.execute("""
            INSERT INTO Ingresos (codigo, habitacion, cama, fecha_ingreso, codigo_paciente, codigo_medico) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (codigo_ingreso, habitacion, cama, fecha_ingreso, codigo_paciente, codigo_medico))
        conn.commit()
        print("Ingreso guardado correctamente")
    except sqlite3.IntegrityError:
        print("Error al guardar el ingreso")

    conn.close()

# Función para cargar la ventana de ingreso
def cargar_ingreso():
    ventana_ingreso = tk.Toplevel(ventana)
    ventana_ingreso.title("Ingreso de Paciente")

    ttk.Label(ventana_ingreso, text="Código del Ingreso").grid(row=0, column=0)
    entry_codigo_ingreso = ttk.Entry(ventana_ingreso)
    entry_codigo_ingreso.grid(row=0, column=1)

    ttk.Label(ventana_ingreso, text="Código del Paciente").grid(row=1, column=0)

    # Crear un Combobox para elegir el código de paciente (solo los códigos de pacientes existentes)
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo FROM Pacientes")
    lista_codigos_pacientes = [row[0] for row in cursor.fetchall()]
    conn.close()

    combobox_codigo_paciente = ttk.Combobox(ventana_ingreso, values=lista_codigos_pacientes)
    combobox_codigo_paciente.grid(row=1, column=1)

    ttk.Label(ventana_ingreso, text="Habitación").grid(row=2, column=0)
    entry_habitacion = ttk.Entry(ventana_ingreso)
    entry_habitacion.grid(row=2, column=1)

    ttk.Label(ventana_ingreso, text="Cama").grid(row=3, column=0)
    entry_cama = ttk.Entry(ventana_ingreso)
    entry_cama.grid(row=3, column=1)

    ttk.Label(ventana_ingreso, text="Fecha de Ingreso").grid(row=4, column=0)
    
    fecha_ingreso = datetime.datetime.now().strftime("%Y-%m-%d") #fecha actual
    
    label_fecha_ingreso = ttk.Label(ventana_ingreso, text=fecha_ingreso) #solo lectura, la fecha
    label_fecha_ingreso.grid(row=4, column=1)

    ttk.Label(ventana_ingreso, text="Código del Médico").grid(row=5, column=0)
    
    # Crear un Combobox para elegir el código del médico
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo FROM Medicos")
    lista_codigos_medicos = [row[0] for row in cursor.fetchall()]
    conn.close()

    combobox_codigo_medico = ttk.Combobox(ventana_ingreso, values=lista_codigos_medicos)
    combobox_codigo_medico.grid(row=5, column=1)

    ttk.Button(ventana_ingreso, text="Guardar", command=lambda: guardar_ingreso(entry_codigo_ingreso.get(), entry_habitacion.get(), entry_cama.get(), fecha_ingreso, combobox_codigo_paciente.get(), combobox_codigo_medico.get())).grid(row=6, column=0, columnspan=2)
    ttk.Button(ventana_ingreso, text="Cancelar", command=ventana_ingreso.destroy).grid(row=7, column=0, columnspan=2)

# Función para cargar la ventana de alta de paciente
def cargar_alta():
    ventana_alta = tk.Toplevel(ventana)
    ventana_alta.title("Dar Alta a Paciente")

    ttk.Label(ventana_alta, text="Fecha de Alta").grid(row=0, column=0)
    
    fecha_alta = datetime.datetime.now().strftime("%Y-%m-%d")
    
    label_fecha_alta = ttk.Label(ventana_alta, text=fecha_alta)
    label_fecha_alta.grid(row=0, column=1)

    ttk.Label(ventana_alta, text="Código del Paciente").grid(row=1, column=0)
    
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo_paciente FROM Ingresos")
    lista_codigos_pacientes_ingresados = [row[0] for row in cursor.fetchall()]
    conn.close()

    combobox_codigo_paciente = ttk.Combobox(ventana_alta, values=lista_codigos_pacientes_ingresados)
    combobox_codigo_paciente.grid(row=1, column=1)

    ttk.Button(ventana_alta, text="Guardar", command=lambda: guardar_alta(fecha_alta, combobox_codigo_paciente.get())).grid(row=2, column=0, columnspan=2)
    ttk.Button(ventana_alta, text="Cancelar", command=ventana_alta.destroy).grid(row=3, column=0, columnspan=2)

# Función para guardar el alta
def guardar_alta(fecha_alta, codigo_paciente):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM Ingresos WHERE codigo_paciente=?", (codigo_paciente,))
    if cursor.fetchone()[0] == 0:
        print("Error: El paciente no está ingresado.")
        conn.close()
        return

    try:
        cursor.execute("""INSERT INTO Altas (codigo_paciente, fecha_alta) VALUES (?, ?)""", (codigo_paciente, fecha_alta)) 
              # Insertar el alta en la tabla Altas


        # Eliminar al paciente de la tabla Ingresos
        cursor.execute("DELETE FROM Ingresos WHERE codigo_paciente=?", (codigo_paciente,))

        conn.commit()
        print("Alta registrada correctamente")
    except sqlite3.Error as e:
        print(f"Error al registrar la alta: {e}")
    
    conn.close()

def mostrar_pacientes_por_medico():
    ventana_informe_pacientes = tk.Toplevel(ventana)
    ventana_informe_pacientes.title("Pacientes Ingresados por Médico")

    ttk.Label(ventana_informe_pacientes, text="Selecciona un Médico:").grid(row=0, column=0, padx=10, pady=10)

    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT codigo FROM Medicos")  # Solo traemos el código del médico
    medicos = cursor.fetchall() #resultados de codigos de medicos
    conn.close()

    lista_medicos = [str(medico[0]) for medico in medicos]  # Extrae solo los códigos
    combobox_medico = ttk.Combobox(ventana_informe_pacientes, values=lista_medicos)
    combobox_medico.grid(row=0, column=1, padx=10, pady=10)

    # Botón para mostrar los pacientes al seleccionar un médico
    def mostrar_pacientes():
        # Obtener el código del médico seleccionado
        codigo_medico = combobox_medico.get()

        if not codigo_medico:
            tk.messagebox.showwarning("Advertencia", "Debe seleccionar un médico.")
            return

        # Obtener los pacientes ingresados por el médico desde la tabla 'Ingresos'
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Ingresos.codigo, Ingresos.habitacion, Ingresos.cama, Ingresos.codigo_paciente
            FROM Ingresos
            WHERE Ingresos.codigo_medico = ?
        """, (codigo_medico,))
        pacientes_ingresados = cursor.fetchall()
        conn.close()

        if not pacientes_ingresados:
            tk.messagebox.showinfo("No se encontró", "No se encontró a ningún paciente ingresado por este médico.")
            return

        #tabla visual para mostrar los datos del paciente
        tree = ttk.Treeview(ventana_informe_pacientes, columns=("Código Ingreso", "Habitación", "Cama", "Código Paciente"), show="headings")
        tree.heading("Código Ingreso", text="Código Ingreso") #establece los encabezados de las columnas
        tree.heading("Habitación", text="Habitación")
        tree.heading("Cama", text="Cama")
        tree.heading("Código Paciente", text="Código Paciente")
        tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Insertar los datos de los pacientes en el Treeview
        for paciente in pacientes_ingresados:
            tree.insert("", tk.END, values=paciente)

    # Botón para mostrar los pacientes
    ttk.Button(ventana_informe_pacientes, text="Mostrar Pacientes", command=mostrar_pacientes).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Botón para cerrar la ventana
    ttk.Button(ventana_informe_pacientes, text="Cerrar", command=ventana_informe_pacientes.destroy).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

def mostrar_pacientes_por_fechas():
    # Crear una ventana para mostrar los pacientes por fechas
    ventana_informe_fechas = tk.Toplevel(ventana)
    ventana_informe_fechas.title("Pacientes Ingresados por Fechas")

    ttk.Label(ventana_informe_fechas, text="Fecha de Inicio (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(ventana_informe_fechas, text="Fecha de Fin (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)

    # Crear los campos de entrada para las fechas
    fecha_inicio_entry = ttk.Entry(ventana_informe_fechas)
    fecha_inicio_entry.grid(row=0, column=1, padx=10, pady=10)
    fecha_fin_entry = ttk.Entry(ventana_informe_fechas)
    fecha_fin_entry.grid(row=1, column=1, padx=10, pady=10)

    # Botón para mostrar los pacientes por fechas
    def mostrar_pacientes_por_rango():
        fecha_inicio = fecha_inicio_entry.get()
        fecha_fin = fecha_fin_entry.get()

        try:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese las fechas en el formato correcto (YYYY-MM-DD).")
            return

        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.")
            return

        # Consultar la base de datos para obtener los pacientes ingresados dentro del rango de fechas
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Ingresos.codigo, Ingresos.habitacion, Ingresos.cama, Ingresos.codigo_paciente, Ingresos.fecha_ingreso
            FROM Ingresos
            WHERE Ingresos.fecha_ingreso BETWEEN ? AND ?
        """, (fecha_inicio.date(), fecha_fin.date()))
        pacientes_ingresados = cursor.fetchall()
        conn.close()

        if not pacientes_ingresados:
            messagebox.showinfo("No se encontró", "No se encontró ningún paciente ingresado en este rango de fechas.")
            return

        tree = ttk.Treeview(ventana_informe_fechas, columns=("Código Ingreso", "Habitación", "Cama", "Código Paciente", "Fecha Ingreso"), show="headings")
        tree.heading("Código Ingreso", text="Código Ingreso") #establece los encabezados de las columnas
        tree.heading("Habitación", text="Habitación")
        tree.heading("Cama", text="Cama")
        tree.heading("Código Paciente", text="Código Paciente")
        tree.heading("Fecha Ingreso", text="Fecha Ingreso")
        tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        for paciente in pacientes_ingresados:
            tree.insert("", tk.END, values=paciente)

    # Botón para mostrar los pacientes por fecha
    ttk.Button(ventana_informe_fechas, text="Mostrar Pacientes", command=mostrar_pacientes_por_rango).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    ttk.Button(ventana_informe_fechas, text="Cerrar", command=ventana_informe_fechas.destroy).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
def mostrar_pacientes_dados_alta_rango():
    ventana_informe_altas = tk.Toplevel(ventana)
    ventana_informe_altas.title("Pacientes Dados de Alta entre Fechas")

    ttk.Label(ventana_informe_altas, text="Fecha de Inicio (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=10)
    ttk.Label(ventana_informe_altas, text="Fecha de Fin (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10)

    fecha_inicio_entry = ttk.Entry(ventana_informe_altas)
    fecha_inicio_entry.grid(row=0, column=1, padx=10, pady=10)
    fecha_fin_entry = ttk.Entry(ventana_informe_altas)
    fecha_fin_entry.grid(row=1, column=1, padx=10, pady=10)

    # Función para mostrar los pacientes dados de alta en el rango de fechas
    def mostrar_altas_por_rango():
        fecha_inicio = fecha_inicio_entry.get()
        fecha_fin = fecha_fin_entry.get()

        try:
            fecha_inicio = datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.datetime.strptime(fecha_fin, "%Y-%m-%d")

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese las fechas en el formato correcto (YYYY-MM-DD).")
            return

        if fecha_inicio > fecha_fin:
            messagebox.showerror("Error", "La fecha de inicio no puede ser mayor que la fecha de fin.")
            return

        # Consultar la base de datos para obtener los pacientes dados de alta dentro del rango de fechas
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT altas.codigo_paciente, altas.fecha_alta   
            FROM altas
            WHERE altas.fecha_alta BETWEEN ? AND ?
        """, #between devuelve los valores entre las dos fechas 
        (fecha_inicio.date(), fecha_fin.date()))
        pacientes_dados_alta = cursor.fetchall()
        conn.close()

        if not pacientes_dados_alta:
            messagebox.showinfo("No se encontró", "No se encontró ningún paciente dado de alta en este rango de fechas.")
            return

        tree = ttk.Treeview(ventana_informe_altas, columns=("Código Paciente", "Fecha Alta"), show="headings")
        tree.heading("Código Paciente", text="Código Paciente")
        tree.heading("Fecha Alta", text="Fecha Alta")
        tree.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        for paciente in pacientes_dados_alta:
            tree.insert("", tk.END, values=paciente)

    ttk.Button(ventana_informe_altas, text="Mostrar Altas", command=mostrar_altas_por_rango).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    ttk.Button(ventana_informe_altas, text="Cerrar", command=ventana_informe_altas.destroy).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Función para mostrar médicos por código
def mostrar_medicos_por_codigo():
    ventana_medicos_codigo = tk.Toplevel(ventana)
    ventana_medicos_codigo.title("Lista de Médicos por Código")
    
    tree = ttk.Treeview(ventana_medicos_codigo, columns=("Código", "Nombre", "Matrícula"), show="headings")
    
    #encabezados de las columnas
    tree.heading("Código", text="Código")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Matrícula", text="Matrícula")
    
    # Configurar el ancho de las columnas
    tree.column("Código", width=100, anchor="center")
    tree.column("Nombre", width=200, anchor="w")
    tree.column("Matrícula", width=150, anchor="center")
    
    # Colocar el Treeview en la ventana
    tree.grid(row=0, column=0, padx=10, pady=10)

    # Función para obtener los médicos y mostrarlos en el Treeview
    def cargar_medicos():
        # Conectar a la base de datos y obtener los médicos ordenados por código
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT codigo, nombre, matricula FROM medicos ORDER BY codigo ASC")  #ascendente
        medicos = cursor.fetchall() #guarda los datos en la variable medico
        conn.close()

        # Limpiar el Treeview antes de agregar nuevos datos
        for item in tree.get_children():
            tree.delete(item)

        if medicos:
            for medico in medicos:
                tree.insert("", tk.END, values=(medico[0], f"{medico[1]}", f"{medico[2]}"))
        else:
            tree.insert("", tk.END, values=("No se encontraron médicos.", "", ""))

    cargar_medicos()

    ttk.Button(ventana_medicos_codigo, text="Cerrar", command=ventana_medicos_codigo.destroy).grid(row=1, column=0, padx=10, pady=10)
# Función para mostrar médicos por nombre
def mostrar_medicos_por_nombre():
    ventana_medicos_nombre = tk.Toplevel(ventana)
    ventana_medicos_nombre.title("Lista de Médicos por Nombre")
    
    tree = ttk.Treeview(ventana_medicos_nombre, columns=("Nombre", "Matrícula", "Código"), show="headings")
    
    # encabezados de las columnas
    tree.heading("Nombre", text="Nombre")
    tree.heading("Matrícula", text="Matrícula")
    tree.heading("Código", text="Código")
    
    tree.column("Nombre", width=200, anchor="w")
    tree.column("Matrícula", width=150, anchor="center")
    tree.column("Código", width=100, anchor="center")
    
    # Colocar el Treeview en la ventana
    tree.grid(row=0, column=0, padx=10, pady=10)

    def cargar_medicos():
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, matricula, codigo FROM medicos ORDER BY nombre ASC")
        medicos = cursor.fetchall()
        conn.close()

        for item in tree.get_children(): #obtiene todos los elementos del treewiew
            tree.delete(item) # los limpia

        if medicos:
            for medico in medicos:
                tree.insert("", tk.END, values=(medico[0], f"{medico[1]}", f"{medico[2]}"))
        else:
            tree.insert("", tk.END, values=("No se encontraron médicos.", "", ""))

    cargar_medicos()

    ttk.Button(ventana_medicos_nombre, text="Cerrar", command=ventana_medicos_nombre.destroy).grid(row=1, column=0, padx=10, pady=10)
def mostrar_medicos_por_especialidad():
    ventana_medicos_especialidad = tk.Toplevel(ventana)
    ventana_medicos_especialidad.title("Médicos por Especialidad")

    conn = conectar_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT especialidad, nombre, codigo FROM medicos ORDER BY especialidad ASC")
    medicos = cursor.fetchall()
    conn.close()

    if not medicos:
        messagebox.showinfo("No se encontraron médicos", "No se encontraron médicos registrados por especialidad.")
        return

    tree = ttk.Treeview(ventana_medicos_especialidad, columns=("Especialidad", "Nombre", "Código"), show="headings")
    tree.heading("Especialidad", text="Especialidad")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Código", text="Código")
    tree.grid(row=0, column=0, padx=10, pady=10)

    for medico in medicos:
        tree.insert("", tk.END, values=medico)

    ttk.Button(ventana_medicos_especialidad, text="Cerrar", command=ventana_medicos_especialidad.destroy).grid(row=1, column=0, padx=10, pady=10)

# ventana principal
ventana = tk.Tk()
ventana.title("Administración Hospitalaria")
ventana.geometry("500x300")

# el menú
menu = tk.Menu(ventana)
ventana.config(menu=menu)

# Menú ABM 
menu_abm = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="ABM", menu=menu_abm)
menu_abm.add_command(label="Cargar Médico", command=lambda: cargar_medico())
menu_abm.add_command(label="Cargar Paciente", command=lambda: cargar_paciente())

# Menú Movimientos
menu_movimientos = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Movimientos", menu=menu_movimientos)
menu_movimientos.add_command(label="Ingreso", command=cargar_ingreso)
menu_movimientos.add_command(label="Dar Alta a Paciente", command=cargar_alta)

# Menú Informes
menu_informes = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Informes", menu=menu_informes)
menu_informes.add_command(label="Cantidad de camas ocupadas", command=mostrar_informe_camas_ocupadas)
menu_informes.add_command(label="Pacientes ingresados por médico", command=mostrar_pacientes_por_medico)
menu_informes.add_command(label="Pacientes ingresados entre fechas", command=mostrar_pacientes_por_fechas)
menu_informes.add_command(label="Pacientes dados de alta entre fechas", command=mostrar_pacientes_dados_alta_rango)
# submenú Médicos
menu_medicos = tk.Menu(menu_informes, tearoff=0)
menu_informes.add_cascade(label="Médicos", menu=menu_medicos)
menu_medicos.add_command(label="Por Código", command=mostrar_medicos_por_codigo)
menu_medicos.add_command(label="Por Nombre", command=mostrar_medicos_por_nombre)
menu_medicos.add_command(label="Por Especialidad", command=mostrar_medicos_por_especialidad)


# Función de salida
def salir():
    ventana.quit()

menu.add_command(label="Salir", command=salir)

# Función para cargar médicos
def cargar_medico():
    global ventana_cargar_medico, entry_codigo, entry_apellido, entry_nombre, entry_matricula, entry_especialidad
    ventana_cargar_medico = tk.Toplevel(ventana)  
    ventana_cargar_medico.title("Cargar Médico")

    # Etiquetas y campos de entrada para médico
    ttk.Label(ventana_cargar_medico, text="Código").grid(row=0, column=0)
    entry_codigo = ttk.Entry(ventana_cargar_medico)
    entry_codigo.grid(row=0, column=1)

    ttk.Label(ventana_cargar_medico, text="Apellido").grid(row=1, column=0)
    entry_apellido = ttk.Entry(ventana_cargar_medico)
    entry_apellido.grid(row=1, column=1)

    ttk.Label(ventana_cargar_medico, text="Nombre").grid(row=2, column=0)
    entry_nombre = ttk.Entry(ventana_cargar_medico)
    entry_nombre.grid(row=2, column=1)

    ttk.Label(ventana_cargar_medico, text="Matrícula").grid(row=3, column=0)
    entry_matricula = ttk.Entry(ventana_cargar_medico)
    entry_matricula.grid(row=3, column=1)

    ttk.Label(ventana_cargar_medico, text="Especialidad").grid(row=4, column=0)
    entry_especialidad = ttk.Entry(ventana_cargar_medico)
    entry_especialidad.grid(row=4, column=1)

    ttk.Button(ventana_cargar_medico, text="Guardar", command=guardar_medico).grid(row=5, column=0, columnspan=2)
    ttk.Button(ventana_cargar_medico, text="Cancelar", command=cerrar_ventana_medico).grid(row=6, column=0, columnspan=2)

# Función para cargar pacientes
def cargar_paciente():
    global ventana_cargar_paciente, entry_codigo, entry_apellido, entry_nombre, entry_obra_social, entry_nro_obra_social, entry_domicilio, entry_telefono
    ventana_cargar_paciente = tk.Toplevel(ventana)  
    ventana_cargar_paciente.title("Cargar Paciente")

    # Etiquetas y campos de entrada para paciente
    ttk.Label(ventana_cargar_paciente, text="Código").grid(row=0, column=0)
    entry_codigo = ttk.Entry(ventana_cargar_paciente)
    entry_codigo.grid(row=0, column=1) #grid posiciona cada elemento

    ttk.Label(ventana_cargar_paciente, text="Apellido").grid(row=1, column=0)
    entry_apellido = ttk.Entry(ventana_cargar_paciente)
    entry_apellido.grid(row=1, column=1)

    ttk.Label(ventana_cargar_paciente, text="Nombre").grid(row=2, column=0)
    entry_nombre = ttk.Entry(ventana_cargar_paciente)
    entry_nombre.grid(row=2, column=1)

    ttk.Label(ventana_cargar_paciente, text="Obra Social").grid(row=3, column=0)
    entry_obra_social = ttk.Entry(ventana_cargar_paciente)
    entry_obra_social.grid(row=3, column=1)

    ttk.Label(ventana_cargar_paciente, text="Número de Obra Social").grid(row=4, column=0)
    entry_nro_obra_social = ttk.Entry(ventana_cargar_paciente)
    entry_nro_obra_social.grid(row=4, column=1)

    ttk.Label(ventana_cargar_paciente, text="Domicilio").grid(row=5, column=0)
    entry_domicilio = ttk.Entry(ventana_cargar_paciente)
    entry_domicilio.grid(row=5, column=1)

    ttk.Label(ventana_cargar_paciente, text="Teléfono").grid(row=6, column=0)
    entry_telefono = ttk.Entry(ventana_cargar_paciente)
    entry_telefono.grid(row=6, column=1)

    ttk.Button(ventana_cargar_paciente, text="Guardar", command=guardar_paciente).grid(row=7, column=0, columnspan=2)
    ttk.Button(ventana_cargar_paciente, text="Cancelar", command=cerrar_ventana_paciente).grid(row=8, column=0, columnspan=2)


ventana.mainloop()
