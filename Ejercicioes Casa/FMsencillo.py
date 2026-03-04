import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tmap as tm
from sklearn.cluster import KMeans

# Diccionario de categorías para los títulos
nombres_ropa = {
    0: "Camisetas", 1: "Pantalones", 2: "Suéteres", 3: "Vestidos", 4: "Abrigos",
    5: "Sandalias", 6: "Camisas", 7: "Tenis", 8: "Bolsos", 9: "Botines"
}

# ==========================================
# 1. CARGA DEL CONJUNTO DE DATOS
# ==========================================
print("1. Cargando el DataFrame de Pandas...")
# Cargamos el CSV. 
df = pd.read_csv('fashion-mnist_train.csv')

# Tomamos una muestra representativa (10,000) para que tu compu lo procese rápido
df_sample = df.sample(n=10000, random_state=42)

# Separamos características (X) y etiquetas (y)
y = df_sample.iloc[:, 0].values  # Columna 0: La etiqueta
X = df_sample.iloc[:, 1:].values # Columnas 1 al final: Los 784 píxeles

print(f"Datos cargados: {X.shape[0]} imágenes con {X.shape[1]} características (píxeles).")

# ==========================================
# 2. APLICACIÓN DE TMAP SOBRE EL CONJUNTO COMPLETO
# ==========================================
print("\n2. Aplicando TMAP Global (puede tardar unos segundos)...")

# Convertimos a binario (blanco y negro) porque TMAP/MinHash funciona mejor así
X_binario = (X > 127).astype(np.uint8)

# Configuración matemática de TMAP
lf_global = tm.LSHForest(128, 128)
codificador = tm.Minhash(784, 128)

# Generar hashes y crear el mapa
hashes_global = [codificador.from_binary_array(fila) for fila in X_binario]
lf_global.batch_add(hashes_global)
lf_global.index()

# Coordenadas X, Y del mapa 2D global
x_global, y_global, _, _, _ = tm.layout_from_lsh_forest(lf_global)

# Visualizar el TMAP Global
plt.figure(figsize=(9, 7))
scatter = plt.scatter(x_global, y_global, c=y, cmap='tab10', s=10, alpha=0.8)
plt.colorbar(scatter, label="Categorías de Ropa (0-9)")
plt.title("TMAP Global - Todas las categorías mezcladas")
plt.xlabel("TMAP X")
plt.ylabel("TMAP Y")
plt.show() # Cierra esta ventana para continuar con el siguiente paso

# ==========================================
# 3. TMAP Y SUBCLUSTERS PARA TODOS LOS CLUSTERS
# ==========================================
print("\n3. Calculando subclusters para TODAS las categorías...")

# Creamos una cuadrícula de 2 filas y 5 columnas para mostrar las 10 categorías
fig, axes = plt.subplots(2, 5, figsize=(18, 8))
fig.suptitle("Análisis de Subclusters usando TMAP por Categoría", fontsize=16)

# Aplanamos la cuadrícula de ejes para iterar fácilmente sobre ella
axes = axes.flatten()

# Hacemos un ciclo del 0 al 9 (las 10 categorías)
for i in range(10):
    print(f"   -> Procesando {nombres_ropa[i]}...")
    
    # Filtramos las instancias de esta categoría específica
    mascara = (y == i)
    X_subset_bin = X_binario[mascara]
    
    # Configuramos un nuevo TMAP solo para este subset
    lf_local = tm.LSHForest(128, 128)
    hashes_local = [codificador.from_binary_array(fila) for fila in X_subset_bin]
    lf_local.batch_add(hashes_local)
    lf_local.index()
    
    x_local, y_local, _, _, _ = tm.layout_from_lsh_forest(lf_local)
    
    # Aplicamos KMeans para encontrar 3 subclusters dentro de esta categoría
    kmeans = KMeans(n_clusters=3, random_state=42, n_init='auto')
    subclusters = kmeans.fit_predict(np.column_stack((x_local, y_local)))
    
    # Dibujamos en su cuadrito correspondiente
    ax = axes[i]
    ax.scatter(x_local, y_local, c=subclusters, cmap='viridis', s=15, alpha=0.8)
    ax.set_title(f"{nombres_ropa[i]}")
    ax.axis('off') # Ocultamos los ejes para que se vea más limpio

plt.tight_layout()
plt.show()

print("\n¡Análisis completado exitosamente!")
