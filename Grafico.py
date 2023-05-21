import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import tkinter.messagebox as messagebox
import os
import matplotlib.pyplot as plt
import numpy as np

archivo = None  # Variable global para almacenar el archivo seleccionado
imagen_generada = None  # Variable global para almacenar la imagen generada

# Logica para poder cargar el los archivos .csv
def cargar_archivo():
    global archivo  # Declarar la variable como global

    archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    if archivo:
        archivo_nombre = archivo.split("/")[-1]  # Obtener solo el nombre del archivo sin la ruta completa
        archivo_nombre = archivo_nombre[:20] + "..." if len(archivo_nombre) > 20 else archivo_nombre
        boton_cargar.config(text=archivo_nombre)  # Mostrar el nombre del archivo en el botón
        print('Archivo seleccionado:', archivo)

        # obtener las columnas csv
        df = pd.read_csv(archivo)
        columnas = df.columns.tolist()

        # Actualizar los valores del combobox2 con las columnas del archivo
        combobox2['values'] = ['Seleccionar ColumnaxD'] + columnas
        combobox2.current(0)  # establecer la selección inicial en Seleccionar ColumnaxD

# Logica del boton aceptar y validaciones
def aceptar():
    global archivo  # Declarar la variable como global
    global imagen_generada  # Declarar la variable como global

    if boton_cargar.cget("text") == '--Seleccione un archivo csv--':
        messagebox.showerror('Error', 'Por favor seleccione un archivo CSV.')
    elif combobox1.get() == 'Seleccionar Grafica':
        messagebox.showerror('Error', 'Por favor seleccione una gráfica válida.')
    else:
        columna_seleccionada = combobox2.get()
        if columna_seleccionada == 'Seleccionar ColumnaxD':
            messagebox.showerror('Error', 'Por favor seleccione una columna válida.')
        else:
            df = pd.read_csv(archivo)
            data = df.groupby(columna_seleccionada).size()
            plt.figure(figsize=(10, 6))

            if combobox1.get() == "Histograma":
                data.plot(kind='hist')
                plt.title('Histograma')
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.savefig('demo.png')

            elif combobox1.get() == "Poligono de frecuencias":
                plt.plot(data.index, data.values, marker='o')
                plt.title('Poligono de frecuencia')
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.savefig('demo.png')

            elif combobox1.get() == "Ojivas":
                frecuencia = np.cumsum(data)
                plt.plot(data.index, frecuencia, marker='o')
                plt.title('Gráfica de Ojiva')
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.savefig('demo.png')

            elif combobox1.get() == "Grafica de barras":
                data.plot(kind='barh')
                plt.title('Grafica de barras')
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.savefig('demo.png')
            elif combobox1.get()=="Grafica de pastel":
                grafica_pastel(data)
                plt.title('Grafica de Pastel')
                plt.savefig('demo.png')

            # Guardar la imagen generada en la variable imagen_generada
            with open('demo.png', 'rb') as file:
                imagen_generada = file.read()

            plt.show()

def grafica_pastel(data):
    labels = data.index
    sizes = data.values
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
# variable a llamar para poder usar la libreria tk
raiz = tk.Tk()
raiz.title('Proyecto xD')

# Color de Bg, bloquear el tamano y asignar por defecto un tamano del cuadro
colorxD = '#FF5858'
raiz.resizable(0, 0)
raiz.geometry('1600x1000')
raiz.configure(background=colorxD)

# Opciones de los combobox
opciones = ['Seleccionar Grafica', 'Histograma', 'Poligono de frecuencias', 'Ojivas', 'Grafica de barras', 'Grafica de pastel']
opciones2 = ['Seleccionar ColumnaxD','id', 'edad', 'xd', 'estatura']

# Botón para subir archivos
boton_cargar = tk.Button(raiz, text='--Seleccione un archivo csv--', command=cargar_archivo, font=('Arial', 14))
boton_cargar.grid(row=0, column=0, padx=80, pady=80, sticky="w")

# Segundo combobox
combobox2 = ttk.Combobox(raiz, values=opciones2, font=('Arial', 20), state='readonly')
combobox2.grid(row=0, column=1, padx=80, pady=80, sticky="w")
combobox2.set(opciones2[0])

# Primer combobox
combobox1 = ttk.Combobox(raiz, values=opciones, font=('Arial', 20), state='readonly')
combobox1.grid(row=0, column=2, padx=80, pady=80, sticky="w")
combobox1.set(opciones[0])

# AceptarxD
boton_aceptar = tk.Button(raiz, text='Aceptar', command=aceptar, font=('Arial', 14))
boton_aceptar.grid(row=0, column=3, padx=80, pady=80, sticky="w")

# ruta de la imagen obviamente xd 
ruta_imagen = os.path.join(os.getcwd(), "linux.png")

# reajustar imagen
imagen = tk.PhotoImage(file=ruta_imagen)
tamano_deseado = (1500, 500)  # Tamano (ancho x alto)
imagen_redimensionada = imagen.subsample(round(imagen.width() / tamano_deseado[0]), round(imagen.height() / tamano_deseado[1]))

# Widget de imagen
imagen_label = tk.Label(raiz, image=imagen_redimensionada)
imagen_label.grid(row=1, column=0, columnspan=4, padx=0, pady=0)  

raiz.mainloop()
