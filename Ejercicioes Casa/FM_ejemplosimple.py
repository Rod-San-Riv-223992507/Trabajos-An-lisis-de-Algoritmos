import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import numpy as np
import matplotlib.pyplot as plt

# --- Variables Globales ---
datos_ropa = [] 
etiquetas_ropa = []

# Diccionario para saber qué significa cada número de etiqueta
nombres_ropa = {
    0: "Camiseta / Top",
    1: "Pantalón",
    2: "Suéter",
    3: "Vestido",
    4: "Abrigo",
    5: "Sandalia",
    6: "Camisa",
    7: "Tenis",
    8: "Bolso",
    9: "Botín"
}

# --- 1. Lógica de Lectura de Datos ---

def cargar_csv():
    global datos_ropa, etiquetas_ropa
    ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    
    if ruta:
        datos_temp = []
        etiquetas_temp = []
        
        try:
            with open(ruta, newline='', encoding='utf-8') as f:
                lector = csv.reader(f)
                
                # Leemos fila por fila
                for fila in lector:
                    try:
                        # Convertimos toda la fila a números enteros
                        fila_numeros = [int(x) for x in fila]
                        
                        # Si la fila tiene 785 números, el primero es la etiqueta
                        if len(fila_numeros) == 785:
                            etiquetas_temp.append(fila_numeros[0])
                            datos_temp.append(fila_numeros[1:]) # Guardamos del 1 al final (784 píxeles)
                        
                        # Si tiene exactamente 784, no tiene etiqueta (solo píxeles)
                        elif len(fila_numeros) == 784:
                            etiquetas_temp.append(-1) # -1 significa "Desconocido"
                            datos_temp.append(fila_numeros)
                            
                    except ValueError:
                        continue # Saltamos la fila si tiene texto (como los encabezados)
            
            if len(datos_temp) == 0:
                messagebox.showerror("Error", "No se encontraron datos válidos de 784/785 columnas.")
            else:
                datos_ropa = datos_temp
                etiquetas_ropa = etiquetas_temp
                lbl_estado.config(text=f"Estado: {len(datos_ropa)} imágenes cargadas.", fg="green")
                messagebox.showinfo("Éxito", "Archivo Fashion MNIST cargado correctamente.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

# --- 2. Lógica de Visualización ---

def mostrar_imagen():
    if not datos_ropa:
        messagebox.showwarning("Atención", "Primero debes cargar un archivo CSV.")
        return
    
    try:
        # Obtenemos el número de índice que el usuario escribió
        indice = int(entrada_indice.get())
        
        # Validamos que el índice exista en nuestra lista
        if indice < 0 or indice >= len(datos_ropa):
            messagebox.showerror("Error", f"Ingresa un número entre 0 y {len(datos_ropa)-1}.")
            return
            
    except ValueError:
        messagebox.showerror("Error", "Por favor ingresa un número de índice válido.")
        return

    # 1. Extraemos los 784 píxeles de esa fila
    pixeles = datos_ropa[indice]
    
    # 2. Convertimos la lista plana en un arreglo de Numpy de 28x28
    imagen_matriz = np.array(pixeles).reshape(28, 28)
    
    # 3. Obtenemos el nombre de la prenda (si tiene etiqueta)
    etiq = etiquetas_ropa[indice]
    nombre_prenda = nombres_ropa.get(etiq, "Desconocido")
    
    # --- Graficar con Matplotlib ---
    plt.figure(f"Visor de Ropa - Imagen {indice}")
    
    # imshow (Image Show) dibuja la matriz de números como colores.
    # cmap='gray' le dice que los colores van de negro a blanco.
    plt.imshow(imagen_matriz, cmap='gray')
    
    plt.title(f"Imagen {indice}: {nombre_prenda} (Etiqueta: {etiq})")
    plt.axis('off') # Apagamos los ejes (X, Y) porque es una foto, no una gráfica
    plt.show()

# --- 3. Interfaz Gráfica (GUI) ---

ventana = tk.Tk()
ventana.title("Visor Fashion MNIST")
ventana.geometry("350x300")

# Sección de Carga
frame_carga = tk.LabelFrame(ventana, text="1. Cargar Datos", padx=10, pady=10)
frame_carga.pack(pady=10, fill="x", padx=10)

btn_cargar = tk.Button(frame_carga, text="Cargar CSV (Fashion MNIST)", command=cargar_csv)
btn_cargar.pack()

lbl_estado = tk.Label(frame_carga, text="Estado: Esperando archivo...", fg="red")
lbl_estado.pack(pady=5)

# Sección de Visualización
frame_ver = tk.LabelFrame(ventana, text="2. Visualizar Prenda", padx=10, pady=10)
frame_ver.pack(pady=10, fill="x", padx=10)

tk.Label(frame_ver, text="¿Qué número de fila quieres ver?").pack()

entrada_indice = tk.Entry(frame_ver, width=10, justify="center")
entrada_indice.insert(0, "0") # Ponemos el 0 por defecto
entrada_indice.pack(pady=5)

btn_mostrar = tk.Button(frame_ver, text="MOSTRAR IMAGEN", command=mostrar_imagen, bg="#2196F3", fg="white", font=("Arial", 10, "bold"))
btn_mostrar.pack(pady=5)

ventana.mainloop()