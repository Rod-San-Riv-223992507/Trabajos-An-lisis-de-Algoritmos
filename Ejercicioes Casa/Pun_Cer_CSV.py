import tkinter as tk
from tkinter import filedialog, messagebox
import math
import csv
import matplotlib.pyplot as plt

# --- Variables Globales ---
datos_csv = [] # Aquí guardaremos los datos si se cargan por archivo

# --- 1. Lógica del Algoritmo ---

def calcular_distancia(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def cargar_archivo_csv():
    global datos_csv
    
    # Abrir ventana para buscar el archivo
    ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    
    if ruta:
        datos_temp = []
        try:
            with open(ruta, newline='') as f:
                lector = csv.reader(f)
                for fila in lector:
                    try:
                        # Convertimos a float. Asumimos formato: x, y
                        x = float(fila[0])
                        y = float(fila[1])
                        datos_temp.append((x, y))
                    except ValueError:
                        continue # Saltamos encabezados o textos
            
            if len(datos_temp) < 2:
                messagebox.showerror("Error", "El archivo debe tener al menos 2 puntos numéricos.")
            else:
                datos_csv = datos_temp
                lbl_estado.config(text=f"Estado: Archivo cargado ({len(datos_csv)} puntos)", fg="green")
                messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

def procesar_datos():
    lista_puntos = []
    
    # DECISIÓN: ¿Usamos CSV o Manual?
    if datos_csv:
        # Si hay datos en el CSV, usamos esos
        lista_puntos = datos_csv
    else:
        # Si no, intentamos leer las cajitas manuales
        try:
            for i in range(5):
                # Solo leemos si las casillas no están vacías
                val_x = entradas_x[i].get()
                val_y = entradas_y[i].get()
                if val_x and val_y:
                    lista_puntos.append((float(val_x), float(val_y)))
        except ValueError:
            messagebox.showerror("Error", "Revisa que los datos manuales sean números.")
            return

    # Validar que tengamos suficientes puntos
    if len(lista_puntos) < 2:
        messagebox.showwarning("Atención", "Se necesitan al menos 2 puntos para calcular.")
        return

    # --- Algoritmo de Fuerza Bruta ---
    n = len(lista_puntos)
    min_distancia = float('inf')
    pareja_ganadora = (None, None)

    for i in range(n):
        for j in range(i + 1, n):
            d = calcular_distancia(lista_puntos[i], lista_puntos[j])
            if d < min_distancia:
                min_distancia = d
                pareja_ganadora = (lista_puntos[i], lista_puntos[j])

    # --- Mostrar Resultados ---
    p1 = pareja_ganadora[0]
    p2 = pareja_ganadora[1]
    
    texto = f"Distancia Mínima: {min_distancia:.4f}\n"
    texto += f"Punto A: {p1}\n"
    texto += f"Punto B: {p2}"
    
    lbl_resultado.config(text=texto, fg="blue")

    # --- Graficar ---
    graficar(lista_puntos, p1, p2)

def graficar(todos, p1, p2):
    x_val = [p[0] for p in todos]
    y_val = [p[1] for p in todos]
    
    plt.figure("Resultado Visual")
    plt.scatter(x_val, y_val, color='blue', label='Puntos')
    plt.scatter([p1[0], p2[0]], [p1[1], p2[1]], color='red', s=100, label='Más Cercanos')
    plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='red', linestyle='--')
    
    plt.title(f"Distancia: {calcular_distancia(p1, p2):.2f}")
    plt.legend()
    plt.grid(True)
    plt.show()

def limpiar_todo():
    """Reinicia todo para poder elegir entre manual o CSV de nuevo"""
    global datos_csv
    datos_csv = [] # Borramos la memoria del CSV
    lbl_estado.config(text="Estado: Usando entrada manual", fg="black")
    lbl_resultado.config(text="---")
    
    # Limpiamos las cajas de texto
    for i in range(5):
        entradas_x[i].delete(0, tk.END)
        entradas_y[i].delete(0, tk.END)

# --- 2. Interfaz Gráfica ---

ventana = tk.Tk()
ventana.title("Par Más Cercano (CSV + Manual)")
ventana.geometry("350x550")

# --- SECCIÓN MANUAL ---
frame_manual = tk.LabelFrame(ventana, text="Opción A: Manual (5 Puntos)", padx=5, pady=5)
frame_manual.pack(pady=10)

entradas_x = []
entradas_y = []

tk.Label(frame_manual, text="X").grid(row=0, column=1)
tk.Label(frame_manual, text="Y").grid(row=0, column=2)

for i in range(5):
    tk.Label(frame_manual, text=f"P {i+1}").grid(row=i+1, column=0)
    ex = tk.Entry(frame_manual, width=8)
    ex.grid(row=i+1, column=1, padx=2)
    entradas_x.append(ex)
    ey = tk.Entry(frame_manual, width=8)
    ey.grid(row=i+1, column=2, padx=2)
    entradas_y.append(ey)

# --- SECCIÓN CSV ---
frame_csv = tk.LabelFrame(ventana, text="Opción B: Archivo CSV", padx=5, pady=5)
frame_csv.pack(pady=10, fill="x", padx=10)

btn_csv = tk.Button(frame_csv, text="Cargar CSV", command=cargar_archivo_csv)
btn_csv.pack()

lbl_estado = tk.Label(frame_csv, text="Estado: Usando entrada manual", fg="black")
lbl_estado.pack(pady=5)

# --- BOTONES DE ACCIÓN ---
tk.Button(ventana, text="CALCULAR DISTANCIA", command=procesar_datos, bg="#4CAF50", fg="white").pack(pady=10)
tk.Button(ventana, text="Limpiar / Reiniciar", command=limpiar_todo).pack(pady=5)

lbl_resultado = tk.Label(ventana, text="---", font=("Arial", 10))
lbl_resultado.pack(pady=10)

ventana.mainloop()