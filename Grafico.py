import math
import tkinter as tk
from tkinter import ttk, filedialog
import pandas as pd
import tkinter.messagebox as messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import Frecuency
import Statistics
from PIL import ImageTk, Image

archivo = None
imagen_generada = None
boton_descargar = None


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
        data = df[columna_seleccionada].dtype
        if data == 'object':
            combobox1['values'] = opciones
            print("String")
        else:
            combobox1['values'] = opciones_cuantitativas
            print("int or float")

def descargar_csv(tabla_frecuencias):
    archivo_guardar = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV File', '*.csv')])
    if archivo_guardar:
        tabla_frecuencias.to_csv(archivo_guardar, index=False)
        messagebox.showinfo('Éxito', 'Archivo CSV guardado correctamente.')


def cal(columna_seleccionada, seleccion):
    df = pd.read_csv(archivo)
    data_column = df.groupby(columna_seleccionada).size()
    data = data_column.index.tolist()
    data_type = df[columna_seleccionada].dtype
    data_number = df[columna_seleccionada]
    array_relative = []
    array_lower = []
    array_superior = []
    mark = []
    range_type = None
    number_class = Frecuency.number_class(len(data_number))
    print(seleccion)
    if data_type == 'object':
        absolute_frecuency = data_column.values.tolist()
        for i in absolute_frecuency:
            result = Frecuency.relative_frecuency(i, len(data_number))
            array_relative.append(result)
    else:
        range_type = Frecuency.range(data)
        width_class = Frecuency.width_class(number_class, range_type, data_type)
        limit_lower = min(data)
        for i in range(number_class):
            limit_lower, limite_superior = Frecuency.limits(limit_lower, width_class)
            mark_class = Frecuency.class_mark(limit_lower, limite_superior)
            array_lower.append(limit_lower)
            array_superior.append(limite_superior)
            mark.append(mark_class)
            print(limit_lower)
            limit_lower = limite_superior
            print(limit_lower)
        absolute_frecuency = Frecuency.absolute_frecuency(data_number, array_lower, array_superior)
        for i in absolute_frecuency:
            result = Frecuency.relative_frecuency(i, len(data_number))
            array_relative.append(result)
    return range_type, number_class, data_column, data, data_type, data_number, array_relative, array_lower, array_superior, mark, absolute_frecuency


def cualitative_mode_parametrics(data):
    colores = np.array(data.index.tolist())
    valores = np.array(data.values.tolist())

    maximo_valor = np.amax(valores)
    indice_maximo = np.argmax(valores)

    color_maximo = colores[indice_maximo]
    print(maximo_valor)
    print(color_maximo)
    return maximo_valor, color_maximo


def cualitative_mode_statics(data):
    print(data)
    df = pd.DataFrame({'Nombre': data.values.tolist()})
    conteo = df.groupby('Nombre').size()
    colors = np.array(conteo.index.tolist())
    valors = np.array(conteo.values.tolist())

    maximo_valor = np.amax(valors)
    indice_maximo = np.argmax(valors)

    color_maximo = colors[indice_maximo]
    print(conteo)
    return maximo_valor, color_maximo

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
            fig = plt.figure(figsize=(20, 10))
            range_type, number_data, data_column, data, data_type, data_number, array_relative, array_lower, array_superior, mark, absolute_frecuency = cal(
                columna_seleccionada, combobox1.get())
            if combobox1.get() == "Histograma":

                print(absolute_frecuency)
                print(mark)
                mark.append(mark[-1] + (mark[-1] - mark[-2]))
                bin_edges = np.array(mark)

                bar_width = np.min(np.diff(bin_edges)) * 0.7  # Ajusta el factor multiplicativo según tus necesidades

                bar_centers = mark[:-1]  # Usamos las marcas de clase directamente como las posiciones de las barras

                plt.bar(bar_centers, absolute_frecuency, width=bar_width, color='#B695C0', align='center')
                plt.xticks(mark[:-1])  # Establecemos las marcas de clase como las etiquetas en el eje x
                plt.title('Histograma')
                plt.grid(True)
                plt.savefig('Histograma.png')
                imagen_generada = convertir_imagen_plt(fig)




            elif combobox1.get() == "Poligono":
                mark.insert(0, mark[0] - (mark[1] - mark[0]))
                mark.append(mark[-1] + (mark[-1] - mark[-2]))
                mark = mark[:-1]

                array_relative.insert(0, 0)
                array_relative = array_relative[:len(mark) - 1]
                array_relative.append(0)

                ranges = np.arange(len(mark))
                plt.plot(ranges, array_relative, marker='o', color='#B695C0', linewidth=3)
                plt.title('Poligono de frecuencia')
                plt.xticks(ranges, labels=mark, rotation=45)
                plt.ylim(0, max(array_relative) + 1)  # Ajuste del límite superior
                plt.grid(True)
                plt.savefig('Poligono.png')
                imagen_generada = convertir_imagen_plt(fig)






            elif combobox1.get() == "Ojiva":
                array_relative.insert(0, 0)
                frecuency_acu = np.cumsum(array_relative)
                print(frecuency_acu)
                limites_x = [0] + mark
                ranges = np.arange(len(limites_x))
                plt.plot(ranges, frecuency_acu, marker='o', color='#B695C0', linewidth=3)
                plt.title('Gráfica de Ojiva')
                plt.ylim(0, max(frecuency_acu))
                plt.xticks(ranges, labels=limites_x, rotation=45)
                plt.grid(True)
                plt.savefig('Ojiva.png')
                imagen_generada = convertir_imagen_plt(fig)

            elif combobox1.get() == "Grafico de Barras":
                print("TIPO DE COLUMNA")
                print(data_type)
                data_column.plot(x=data_column.index.tolist(), y=data_column.values.tolist(), kind="barh", color='#B695C0')
                plt.title('Grafica de barras')
                plt.xticks(rotation=45)
                plt.grid(True)
                plt.savefig('Grafico de Barras.png')
                imagen_generada = convertir_imagen_plt(fig)

            elif combobox1.get() == "Grafico de Pastel":
                print("PASTEL")
                if data_type == 'object':
                    Pie_graphics = []
                    for i in data_column.values.tolist():
                        result = Frecuency.relative_frecuency(i, len(data_number))
                        Pie_graphics.append(result)
                    cmap = plt.get_cmap('tab20')
                    colors = cmap(np.linspace(0, 1, len(Pie_graphics)))
                    plt.pie(Pie_graphics, labels=[''] * len(data), autopct='%1.1f%%', startangle=140, colors=colors, shadow=True, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
                    plt.legend(data, fancybox=True, framealpha=1, shadow=True, borderpad=1)
                else:
                    cmap = plt.get_cmap('tab20')
                    colors = cmap(np.linspace(0, 1, len(absolute_frecuency)))
                    plt.pie(absolute_frecuency, labels=[''] * len(mark), autopct='%1.1f%%', startangle=140, colors=colors, shadow=True, wedgeprops={'linewidth': 1, 'edgecolor': 'white'} )
                    plt.legend(mark, fancybox=True, framealpha=1, shadow=True, borderpad=1)
                plt.axis('equal')
                plt.title('Grafica de Pastel')
                plt.savefig('Grafico de Pastel.png')
                imagen_generada = convertir_imagen_plt(fig)
            plt.close(fig)
            messagebox.showinfo('Éxito', 'Operación exitosa')
            return columna_seleccionada, combobox1.get()


def statics():
    columna_seleccionada, seleccion = aceptar()
    range_type, number_class, data_column, data, data_type, data_number, array_relative, array_lower, array_superior, mark, absolute_frecuency = cal(
        columna_seleccionada, seleccion)

    ventana_emergente = tk.Toplevel(raiz)
    ventana_emergente.title('DATOS')
    conglomerates = Statistics.get_conglomerates(data_number, 100)
    if data_type == 'object' or seleccion == 'Grafico de Barras' or seleccion == 'Grafico de Pastel':
        ventana_emergente.geometry("300x200")
        maximo_valor, color_maximo = cualitative_mode_parametrics(data_column)
        max_value, values = cualitative_mode_statics(conglomerates)
        datos_resultados = [
            ("---------Datos Parametricos---------", ''),
            ("Moda: ", color_maximo),
            ("Cantidad: ", maximo_valor),
            ("---------Datos Estadisticos---------", ''),
            ("Moda:", values),
            ("Cantidad: ", max_value),
        ]

        popup(datos_resultados, ventana_emergente)
    else:
        ventana_emergente.geometry("1200x300")
        init = Statistics.bias(data_number)
        if init > 0:
            bine = "Sesgo a la derecha"
        elif init == 0:
            bine = "Al centro"
        else:
            bine = "Sesgo a la izquierda"

        print(array_relative)
        print(mark)
        median_par = Statistics.promedio(mark, absolute_frecuency, len(data_number))
        mediana_par = Statistics.median(mark)
        moda_par = Statistics.moda(absolute_frecuency, mark)
        rango_par = range_type
        varianza_par = Statistics.variance_all(mark, absolute_frecuency, len(data_number), median_par)


        media, mediana, moda, rango, varianza = Agrupaciones(conglomerates)

        inite = Statistics.bias(conglomerates)
        if inite > 0:
            bine_all = "Sesgo a la derecha"
        elif inite == 0:
            bine_all = "Al centro"
        else:
            bine_all = "Sesgo a la izquierda"

        geometry_all = try_parameters(data_number)
        geometry_all_es = try_funcion(conglomerates)

        datos_resultados = [
            ("---------Datos Parametricos---------", ''),
            ("Media:", Statistics.mean(data_number)),
            ("Mediana:", Statistics.median(data_number)),
            ("Moda:", Statistics.mode(data_number)),
            ("Varianza:", Statistics.variance_p(data_number, Statistics.mean(data_number))),
            ("Desviación estándar:", Statistics.standard_deviation(data_number)),
            ("Geométrica:", geometry_all),
            ("Media truncada:", Statistics.truncated_mean(data_number)),
            ("Sesgo:", bine),
            ("Rango:", Frecuency.range(data_number)),
            ("---------Datos Estadisticos---------", ''),
            ("Media:", Statistics.mean(conglomerates)),
            ("Mediana:", Statistics.median(conglomerates)),
            ("Moda:", Statistics.mode(conglomerates)),
            ("Varianza:", Statistics.variance(conglomerates)),
            ("Desviación estándar:", Statistics.standard_deviation(conglomerates)),
            ("Geométrica:", geometry_all_es),
            ("Media truncada:", Statistics.truncated_mean(conglomerates)),
            ("Sesgo:", bine_all),
            ("Rango:", Frecuency.range(conglomerates)),
        ]

        agrupados = [
            ("---------Datos Estadisticos agrupados---------", ''),
            ("Media:", media),
            ("Mediana:", mediana),
            ("Moda:", moda),
            ("Varianza:", varianza),
            ("Desviación estándar:", math.sqrt(varianza)),
            ("Rango:", rango),
            ("---------Datos Parametricos agrupados---------", ''),
            ("Media:", median_par),
            ("Mediana:", mediana_par),
            ("Moda:", moda_par),
            ("Varianza:", varianza_par),
            ("Desviación estándar:", math.sqrt(varianza_par)),
            ("Rango:", rango_par),
        ]

        temporal_graphics(data, "Grafica Parametricos")
        print("HOLACOMOESTAS")
        print(agrupados)
        print(datos_resultados)
        popup(agrupados, ventana_emergente)
        popup(datos_resultados, ventana_emergente)
        mostrar_imagen("Grafica Parametricos.png", "Grafica Parametricos")
        mostrar_imagen("Grafica Estasdistica.png", "Grafica Estasdistica")
    return


def try_funcion(conglomerates):
    try:
        geometry_all_es = Statistics.geometry(conglomerates)
        print("HOLACOMOESTAS3")
        return geometry_all_es
    except ValueError as e:
        print("HOLACOMOESTAS4")
        geometry_all_es = "La media no se puede realizar"
        return geometry_all_es

def try_parameters(data_number):
    try:
        geometry_all = Statistics.geometry(data_number)
        print("HOLACOMOESTAS1")
        return geometry_all
    except ValueError as e:
        print("HOLACOMOESTAS2")
        geometry_all = "La media no se puede realizar"
        return geometry_all



def mostrar_imagen(ruta_imagen, Title):
    ventana_emergente = tk.Toplevel()
    ventana_emergente.title(Title)

    imagen = Image.open(ruta_imagen)
    imagen = imagen.resize((400, 400), Image.LANCZOS)
    imagen = ImageTk.PhotoImage(imagen)

    etiqueta_imagen = tk.Label(ventana_emergente, image=imagen)
    etiqueta_imagen.image = imagen
    etiqueta_imagen.pack()


def Agrupaciones(column):
    range_type, number_class, data, data_type, data_number, array_relative, array_lower, array_superior, mark, absolute_frecuency = Agruopate_data(
        column)
    df = pd.DataFrame({
        "Clase": list(range(1, number_class + 1)),
        "Limite inferior": array_lower,
        "Limite superior": array_superior,
        "Marca de clase": mark,
        "Frecuencia absoluta": absolute_frecuency,
        "Frecuencia relativa": array_relative
    })
    temporal_graphics(data, "Grafica Estasdistica")
    media = Statistics.promedio(mark, absolute_frecuency, len(data_number))
    mediana = Statistics.median(mark)
    moda = Statistics.moda(absolute_frecuency, mark)
    rango = range_type
    varianza = Statistics.variance_all(mark, absolute_frecuency, len(data_number), media)
    return media, mediana, moda, rango, varianza


def Agruopate_data(column):
    data = column.values.tolist()
    data_type = "int64"
    data_number = column
    array_relative = []
    array_lower = []
    array_superior = []
    mark = []
    number_class = Frecuency.number_class(len(data_number))
    range_type = Frecuency.range(data)
    width_class = Frecuency.width_class(number_class, range_type, data_type)
    limit_lower = min(data)
    for i in range(number_class):
        limit_lower, limite_superior = Frecuency.limits(limit_lower, width_class)
        mark_class = Frecuency.class_mark(limit_lower, limite_superior)
        array_lower.append(limit_lower)
        array_superior.append(limite_superior)
        mark.append(mark_class)
        limit_lower = limite_superior
    absolute_frecuency = Frecuency.absolute_frecuency(data_number, array_lower, array_superior)
    for i in absolute_frecuency:
        result = Frecuency.relative_frecuency(i, len(data_number))
        array_relative.append(result)
    return range_type, number_class, data, data_type, data_number, array_relative, array_lower, array_superior, mark, absolute_frecuency


def temporal_graphics(column_values, title):
    cacl = Statistics.temporal(column_values, 5)
    fig, ax = plt.subplots()
    ax.plot(column_values, label='original')
    ax.plot(cacl, label='error')
    ax.legend()
    plt.savefig(title)
    plt.show()


def popup(datos_resultados, ventana_emergente):
    canvas = tk.Canvas(ventana_emergente)
    canvas.pack(side="left", fill="both", expand=True)

    # Agregar un scrollbar al canvas
    scrollbar = tk.Scrollbar(ventana_emergente, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    # Configurar el canvas para que utilice el scrollbar
    canvas.configure(yscrollcommand=scrollbar.set)

    # Crear un frame para las etiquetas dentro del canvas
    contenedor_etiquetas = tk.Frame(canvas)

    # Agregar el frame al canvas
    canvas.create_window((0, 0), window=contenedor_etiquetas, anchor="nw")

    # Configurar el tamaño máximo del canvas
    canvas.configure(scrollregion=canvas.bbox("all"), width=400, height=300)

    # Permitir desplazamiento con el scrollbar
    contenedor_etiquetas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    # Agregar las etiquetas al frame
    for i, (dato, resultado) in enumerate(datos_resultados):
        etiqueta_dato = tk.Label(contenedor_etiquetas, text=dato, font=('Arial', 12))
        etiqueta_dato.grid(row=i, column=0, sticky="w")

        etiqueta_resultado = tk.Label(contenedor_etiquetas, text=str(resultado), font=('Arial', 12))
        etiqueta_resultado.grid(row=i, column=1, sticky="w")


def mostrar_dataframe(df, Title):
    ventana_emergente = tk.Toplevel()
    ventana_emergente.title(Title)

    # Crear tabla
    tabla = ttk.Treeview(ventana_emergente)
    tabla.pack(side=tk.LEFT, fill=tk.BOTH)

    # Configurar encabezados de columna
    encabezados = list(df.columns)
    tabla["columns"] = encabezados
    for col in encabezados:
        tabla.heading(col, text=col)
        tabla.column(col, width=100)  # Establecer ancho fijo de 100 píxeles

    # Agregar filas de datos
    for i, fila in df.iterrows():
        tabla.insert("", "end", text=i, values=list(fila))

    # Agregar barra de desplazamiento vertical
    scrollbar = ttk.Scrollbar(ventana_emergente, orient=tk.VERTICAL, command=tabla.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    tabla.configure(yscrollcommand=scrollbar.set)

    # Mostrar la tabla en la ventana
    tabla.pack()


def dataframe():
    columna_seleccionada, seleccion = aceptar()
    range_type, number_class, data_column, data, data_type, data_number, array_relative, array_lower, array_superior, mark, absolute_frecuency = cal(
        columna_seleccionada, seleccion)
    if data_type == 'object':
        df = pd.DataFrame({
            "Clase": list(range(1, len(data) + 1)),
            "Datos": data,
            "Frecuencia absoluta": absolute_frecuency,
            "Frecuencia relativa": array_relative
        })
    else:
        df = pd.DataFrame({
            "Clase": list(range(1, number_class + 1)),
            "Limite inferior": array_lower,
            "Limite superior": array_superior,
            "Marca de clase": mark,
            "Frecuencia absoluta": absolute_frecuency,
            "Frecuencia relativa": array_relative
        })
    return df


def convertir_imagen_plt(fig):
    # Eliminar marco y widget de imagen existentes
    if hasattr(raiz, 'frame_imagen'):
        raiz.frame_imagen.destroy()

    # Crear un nuevo marco para la imagen
    frame_imagen = tk.Frame(raiz, bg='#FFFFFF')
    frame_imagen.pack(padx=10, pady=10)
    raiz.frame_imagen = frame_imagen

    # Crear el widget de imagen para mostrar la figura
    canvas = FigureCanvasTkAgg(fig, master=frame_imagen)
    canvas.draw()
    imagen_tkinter = canvas.get_tk_widget()
    imagen_tkinter.pack()

    return imagen_tkinter


def mostrar_dataframe_ventana_emergente():
    df = dataframe()
    mostrar_dataframe(df, "ESTADISTICOS")


def Export():
    df = dataframe()
    df.to_csv('tabla.csv', index=False)


opciones = ['Seleccionar Grafica', 'Grafico de Barras', 'Grafico de Pastel']

opciones_cuantitativas = ['Seleccionar Grafica', 'Ojiva', 'Poligono',
                          'Histograma', 'Grafico de Pastel']

raiz = tk.Tk()
raiz.title('Proyecto')
raiz.resizable(True, True)
raiz.geometry('800x500')
raiz.configure(background='#444654')

# Crear un marco para los objetos
frame = tk.Frame(raiz, bg='#444654')
frame.pack(pady=20)

# Crear objetos de la interfaz
boton_cargar = tk.Button(frame, text='Cargar Archivo', command=cargar_archivo, font=('Arial', 14), width=15)
boton_cargar.grid(row=0, column=0, padx=10, pady=10)

combobox2 = ttk.Combobox(frame, values=[], font=('Arial', 14), state='readonly', width=20)
combobox2.grid(row=0, column=1, padx=10, pady=10)
combobox2.set('Seleccionar Columna')
combobox2.bind("<<ComboboxSelected>>", lambda event: obtener_tipo_dato())

combobox1 = ttk.Combobox(frame, values=opciones, font=('Arial', 14), state='readonly', width=20)
combobox1.grid(row=0, column=2, padx=10, pady=10)
combobox1.set('Seleccionar Gráfica')
combobox1.bind("<<ComboboxSelected>>", lambda event: obtener_tipo_dato())

boton_aceptar = tk.Button(frame, text='Aceptar', command=aceptar, font=('Arial', 14), width=10)
boton_aceptar.grid(row=0, column=3, padx=10, pady=10)

boton_tabla = tk.Button(raiz, text="Mostrar Tabla de frecuencia", command=mostrar_dataframe_ventana_emergente)
boton_tabla.pack()

boton_otra_funcion = tk.Button(raiz, text='Parametricos y estadisticos', command=statics)
boton_otra_funcion.pack(padx=10, pady=10)

boton_descargar = tk.Button(raiz, text='Descargar CSV', command=Export,
                            font=('Arial', 14), width=15)
boton_descargar.pack(side="bottom", padx=20, pady=20)

raiz.mainloop()
