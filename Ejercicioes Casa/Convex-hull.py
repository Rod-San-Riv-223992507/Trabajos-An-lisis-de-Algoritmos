import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import matplotlib.pyplot as plt

datos_csv = [] 


def resolver_convex_hull_fuerza_bruta(lista_puntos):
  
    n = len(lista_puntos)
    
    
    if n < 3:
        return lista_puntos, []

    puntos_hull = set() 
    bordes = []

    
    for i in range(n):
        
        for j in range(i + 1, n):
            p1 = lista_puntos[i]
            p2 = lista_puntos[j]

            lado_positivo = False
            lado_negativo = False
            
            for k in range(n):
                if k == i or k == j:
                    continue 
                
                p3 = lista_puntos[k]
                
                d = (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])
                
                if d > 0:
                    lado_positivo = True
                elif d < 0:
                    lado_negativo = True


            if not (lado_positivo and lado_negativo):
                bordes.append((p1, p2))
                puntos_hull.add(p1)
                puntos_hull.add(p2)

    return list(puntos_hull), bordes



def cargar_archivo_csv():
    global datos_csv
    ruta = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])
    
    if ruta:
        datos_temp = []
        try:
            with open(ruta, newline='', encoding='utf-8') as f:
                lector = csv.reader(f)
                for fila in lector:
                    try:
                        x = float(fila[0])
                        y = float(fila[1])
                        datos_temp.append((x, y))
                    except (ValueError, IndexError):
                        continue 
            
            if len(datos_temp) < 3:
                messagebox.showerror("Error", "El Convex Hull necesita al menos 3 puntos.")
            else:
                datos_csv = datos_temp
                lbl_estado.config(text=f"Estado: Archivo cargado ({len(datos_csv)} puntos)", fg="green")
                messagebox.showinfo("Éxito", "Archivo cargado correctamente.")
                
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

def procesar_datos():
    lista_puntos = []
    

    if datos_csv:
        lista_puntos = datos_csv
    else:
        try:
            for i in range(5):
                val_x = entradas_x[i].get()
                val_y = entradas_y[i].get()
                if val_x and val_y:
                    lista_puntos.append((float(val_x), float(val_y)))
        except ValueError:
            messagebox.showerror("Error", "Revisa que los datos manuales sean números.")
            return

    if len(lista_puntos) < 3:
        messagebox.showwarning("Atención", "Se necesitan al menos 3 puntos.")
        return

 
    puntos_hull, bordes = resolver_convex_hull_fuerza_bruta(lista_puntos)

    texto = f"Total de puntos analizados: {len(lista_puntos)}\n"
    texto += f"Puntos en el Convex Hull (La liga): {len(puntos_hull)}\n"
    

    texto += "Vértices detectados:\n"
    for p in puntos_hull[:5]: 
        texto += f"({p[0]}, {p[1]})\n"
    if len(puntos_hull) > 5:
        texto += "... y más."
        
    lbl_resultado.config(text=texto, fg="blue")


    graficar(lista_puntos, puntos_hull, bordes)

def graficar(todos, hull, bordes):
  
    x_todos = [p[0] for p in todos]
    y_todos = [p[1] for p in todos]
    

    x_hull = [p[0] for p in hull]
    y_hull = [p[1] for p in hull]

    plt.figure("Resultado Convex Hull (Fuerza Bruta)")
    

    plt.scatter(x_todos, y_todos, color='blue', label='Puntos Interiores', alpha=0.5)
    

    plt.scatter(x_hull, y_hull, color='red', s=60, label='Vértices (Convex Hull)')
    

    for borde in bordes:
        p1, p2 = borde
        plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='red', linestyle='-', linewidth=2)
    
    plt.title("Envolvente Convexa (Fuerza Bruta)")
    plt.legend()
    plt.grid(True)
    plt.show()

def limpiar_todo():
    global datos_csv
    datos_csv = [] 
    lbl_estado.config(text="Estado: Usando entrada manual", fg="black")
    lbl_resultado.config(text="---")
    for i in range(5):
        entradas_x[i].delete(0, tk.END)
        entradas_y[i].delete(0, tk.END)



ventana = tk.Tk()
ventana.title("Convex Hull - Fuerza Bruta")
ventana.geometry("380x600")


frame_manual = tk.LabelFrame(ventana, text="Opción A: Manual (Mínimo 3)", padx=5, pady=5)
frame_manual.pack(pady=10, fill="x", padx=10)

entradas_x = []
entradas_y = []

tk.Label(frame_manual, text="X").grid(row=0, column=1)
tk.Label(frame_manual, text="Y").grid(row=0, column=2)

for i in range(5):
    tk.Label(frame_manual, text=f"Punto {i+1}").grid(row=i+1, column=0, padx=5)
    ex = tk.Entry(frame_manual, width=10)
    ex.grid(row=i+1, column=1, padx=5, pady=2)
    entradas_x.append(ex)
    ey = tk.Entry(frame_manual, width=10)
    ey.grid(row=i+1, column=2, padx=5, pady=2)
    entradas_y.append(ey)


frame_csv = tk.LabelFrame(ventana, text="Opción B: Archivo CSV", padx=5, pady=5)
frame_csv.pack(pady=10, fill="x", padx=10)

btn_csv = tk.Button(frame_csv, text="Cargar 'puntos.csv'", command=cargar_archivo_csv)
btn_csv.pack(pady=5)

lbl_estado = tk.Label(frame_csv, text="Estado: Usando entrada manual", fg="black")
lbl_estado.pack(pady=5)


tk.Button(ventana, text="CALCULAR CONVEX HULL", command=procesar_datos, bg="#FF5722", fg="white", font=("Arial", 10, "bold")).pack(pady=10)
tk.Button(ventana, text="Limpiar / Reiniciar", command=limpiar_todo).pack(pady=5)


frame_res = tk.LabelFrame(ventana, text="Resultados", padx=5, pady=5)
frame_res.pack(pady=10, fill="both", expand=True, padx=10)

lbl_resultado = tk.Label(frame_res, text="---", font=("Courier", 10), justify="left")
lbl_resultado.pack()

ventana.mainloop()