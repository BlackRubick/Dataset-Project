import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import tkinter.messagebox as messagebox
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import csv

archivo = None
imagen_generada = None
boton_descargar = None  # Variable para el botón de descargar CSV

def cargar_archivo():
    global archivo

    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if archivo:
        archivo_nombre = archivo.split("/")[-1]
        archivo_nombre = archivo_nombre[:20] + "..." if len(archivo_nombre) > 20 else archivo_nombre
        boton_cargar.config(text=archivo_nombre)
        print('Archivo seleccionado:', archivo)

        df = pd.read_csv(archivo)
        columnas = df.columns.tolist()
        combobox2['values'] = ['Seleccionar Columna'] + columnas
        combobox2.current(0)

def obtener_tipo_dato():
    columna_seleccionada = combobox2.get()
    if columna_seleccionada != 'Seleccionar Columna':
        df = pd.read_csv(archivo)
        data = df[columna_seleccionada]
        combobox1['values'] = opciones_cuantitativas
        if combobox1.get() in ['Ojiva', 'Grafico de Barras', 'Grafico de Pastel']:
            boton_tabla.config(state=tk.NORMAL)  # Habilitar el botón de tabla de frecuencias
        else:
            boton_tabla.config(state=tk.DISABLED)  # Deshabilitar el botón de tabla de frecuencias


def generar_tabla_frecuencias():
    columna_seleccionada = combobox2.get()
    df = pd.read_csv(archivo)
    data = df[columna_seleccionada]

    tabla_frecuencias = pd.DataFrame({'clase': data.value_counts().index, 'frecuencia absoluta': data.value_counts().values})
    tabla_frecuencias['frecuencia relativa'] = tabla_frecuencias['frecuencia absoluta'] / len(data) * 100

    suma_total = tabla_frecuencias['frecuencia absoluta'].sum()
    total_row = pd.DataFrame({'clase': ['Total'], 'frecuencia absoluta': [suma_total], 'frecuencia relativa': [100]})
    tabla_frecuencias = pd.concat([tabla_frecuencias, total_row], ignore_index=True)

    messagebox.showinfo('Tabla de Frecuencias', tabla_frecuencias.to_string(index=False))

    global boton_descargar  # Utilizar la variable global del botón de descargar CSV

    if boton_descargar:  # Si el botón ya existe, eliminarlo antes de crear uno nuevo
        boton_descargar.destroy()

    boton_descargar = tk.Button(raiz, text='Descargar CSV', command=lambda: descargar_csv(tabla_frecuencias),
                               font=('Arial', 14))
    boton_descargar.grid(row=1, column=4, padx=80, pady=80, sticky="se")

def descargar_csv(tabla_frecuencias):
    archivo_guardar = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV File', '*.csv')])
    if archivo_guardar:
        tabla_frecuencias.to_csv(archivo_guardar, index=False)
        messagebox.showinfo('Éxito', 'Archivo CSV guardado correctamente.')


def aceptar():
    global archivo
    global imagen_generada

    if boton_cargar.cget("text") == '--Seleccione un archivo csv--':
        messagebox.showerror('Error', 'Por favor seleccione un archivo CSV.')
    elif combobox1.get() == 'Seleccionar Grafica':
        messagebox.showerror('Error', 'Por favor seleccione una gráfica válida.')
    else:
        columna_seleccionada = combobox2.get()
        if columna_seleccionada == 'Seleccionar Columna':
            messagebox.showerror('Error', 'Por favor seleccione una columna válida.')
        else:
            df = pd.read_csv(archivo)
            data = df[columna_seleccionada]
            data_type = data.dtype
            print(data_type)
            fig = plt.figure(figsize=(10, 6))

            if combobox1.get() == "Histograma":
                data.plot(kind='hist')
                plt.title('Histograma')
                plt.xticks(rotation=45)
                plt.grid(True)
                imagen_generada = convertir_imagen_plt(fig)

            elif combobox1.get() == "Poligono":
                plt.plot(data.index, data.values, drawstyle='steps-post')
                plt.title('Poligono')
                plt.xticks(rotation=45)
                plt.grid(True)
                imagen_generada = convertir_imagen_plt(fig)
                boton_tabla.config(state=tk.DISABLED)  # Deshabilitar el botón de tabla de frecuencias

            elif combobox1.get() == "Ojiva":
                frecuencia = np.cumsum(data.value_counts().sort_index())
                plt.plot(data.value_counts().sort_index().index, frecuencia, marker='o')
                plt.title('Ojiva')
                plt.xticks(rotation=45)
                plt.grid(True)
                imagen_generada = convertir_imagen_plt(fig)

            elif combobox1.get() == "Grafico de Barras":
                data.value_counts().sort_index().plot(kind='bar')
                plt.title('Grafico de Barras')
                plt.xticks(rotation=45)
                plt.grid(True)
                imagen_generada = convertir_imagen_plt(fig)

            elif combobox1.get() == "Grafico de Pastel":
                data.value_counts().plot(kind='pie', autopct='%1.1f%%')
                plt.title('Gráfico de Pastel')
                boton_tabla.config(state=tk.DISABLED)  # Deshabilitar el botón de tabla de frecuencias
                imagen_generada = convertir_imagen_plt(fig)

            plt.close(fig)

            imagen_label.configure(image=imagen_generada)
            imagen_label.image = imagen_generada

            messagebox.showinfo('Éxito', 'Gráfica generada correctamente.')


def convertir_imagen_plt(fig):
    canvas = FigureCanvasTkAgg(fig, master=raiz)
    canvas.draw()
    imagen_tkinter = canvas.get_tk_widget()
    imagen_tkinter.grid(row=1, column=0, columnspan=4, padx=0, pady=0)
    return imagen_tkinter

raiz = tk.Tk()
raiz.title('Proyecto')

colorxD = '#FF5858'
raiz.resizable(10, 10)
raiz.geometry('1600x900')
raiz.configure(background=colorxD)

opciones_cualitativas = ['Seleccionar Grafica', 'Grafico de Barras', 'Grafico de Pastel', 'Ojiva']
opciones_cuantitativas = ['Seleccionar Grafica', 'Grafico de Barras', 'Grafico de Pastel', 'Ojiva', 'Poligono', 'Histograma']

boton_cargar = tk.Button(raiz, text='--Seleccione un archivo csv--', command=cargar_archivo, font=('Arial', 14))
boton_cargar.grid(row=0, column=0, padx=80, pady=80, sticky="w")

combobox2 = ttk.Combobox(raiz, values=[], font=('Arial', 20), state='readonly')
combobox2.grid(row=0, column=1, padx=80, pady=80, sticky="w")
combobox2.set('Seleccionar Columna')
combobox2.bind("<<ComboboxSelected>>", lambda event: obtener_tipo_dato())

combobox1 = ttk.Combobox(raiz, values=[], font=('Arial', 20), state='readonly')
combobox1.grid(row=0, column=2, padx=80, pady=80, sticky="w")
combobox1.set('Seleccionar Grafica')
combobox1.bind("<<ComboboxSelected>>", lambda event: obtener_tipo_dato())

boton_aceptar = tk.Button(raiz, text='Aceptar', command=aceptar, font=('Arial', 14))
boton_aceptar.grid(row=0, column=3, padx=80, pady=80, sticky="w")

boton_tabla = tk.Button(raiz, text='Tabla de Frecuencias', command=generar_tabla_frecuencias, font=('Arial', 14), state='disabled')
boton_tabla.grid(row=0, column=4, padx=80, pady=80, sticky="w")

boton_descargar = tk.Button(raiz, text='Descargar CSV', command=lambda: descargar_csv(tabla_frecuencias), font=('Arial', 14))
boton_descargar.grid(row=0, column=5, padx=80, pady=80, sticky="se")  # Agregar el botón en la esquina inferior derecha

imagen_label = tk.Label(raiz)
imagen_label.grid(row=1, column=0, columnspan=4, padx=0, pady=0)

raiz.mainloop()

