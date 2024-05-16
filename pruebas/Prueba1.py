import pyscreenshot as ImageGrab
import numpy as np

# Capturar imagen de la pantalla
imagen = ImageGrab.grab()

# Obtener ancho y alto
width, height = imagen.size

# Definir tamaño de celda
cell_size = 50  

# Calcular número de filas y columnas
num_rows = height // cell_size
num_cols = width // cell_size

# Iterar sobre la cuadrícula
for row in range(num_rows):
    for col in range(num_cols):
        # Calcular coordenadas de la celda
        x0 = col * cell_size
        y0 = row * cell_size
        x1 = x0 + cell_size
        y1 = y0 + cell_size

        # Recortar la imagen
        cell_img = imagen.crop((x0, y0, x1, y1))

        # Convertir a arreglo NumPy
        cell_array = np.array(cell_img)

        # Calcular valores RGB promedio
        mean_r = np.mean(cell_array[:, :, 0])  
        mean_g = np.mean(cell_array[:, :, 1])  
        mean_b = np.mean(cell_array[:, :, 2])  

        print(f"Celda ({row}, {col}): RGB Promedio = ({mean_r:.2f}, {mean_g:.2f}, {mean_b:.2f})")
