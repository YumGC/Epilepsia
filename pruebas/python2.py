import pyscreenshot as ImageGrab
import numpy as np
import time
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QFont, QPalette, QColor  # Importar QFont desde PyQt5.QtGui
from PyQt5.QtCore import Qt


# Definir tamaño de celda y frecuencia de muestreo
cell_size = 50
sample_rate = 3  # 3 Hz

# Variables para almacenar valores previos
prev_mean_rgb = None
threshold = 20  # Umbral para cambios bruscos (ajustable)
warning_shown = False  # Variable para controlar si se mostró la alerta

# Función para mostrar aviso en pantalla
def show_warning():
    global warning_shown
    app = QApplication([])

    # Configuración de la ventana
    window = QWidget()
    window.setWindowTitle("Alerta de Epilepsia")
    window.setStyleSheet("background-color: black;")
    window.showFullScreen()

    # Configuración del texto
    label = QLabel("Alerta: Se detectaron cambios bruscos en la pantalla.")
    label.setFont(QFont('Arial', 48))
    label.setStyleSheet("color: white;")
    label.setAlignment(Qt.AlignCenter)

    # Configuración del botón
    close_button = QPushButton("Cerrar Alerta")
    close_button.setFont(QFont('Arial', 24))
    close_button.setStyleSheet("background-color: darkred; color: white;")
    close_button.clicked.connect(lambda: close_warning(window))

    # Diseño de la ventana
    layout = QVBoxLayout()
    layout.addWidget(label)
    layout.addWidget(close_button)
    window.setLayout(layout)

    warning_shown = True
    app.exec_()

# Función para cerrar la ventana de aviso
def close_warning(root):
    global warning_shown
    root.destroy()
    warning_shown = False
    time.sleep(2)  # Agregar pausa de 2 segundos después de cerrar la ventana
# Bucle principal
while True:
    # Capturar imagen de la pantalla
    imagen = ImageGrab.grab()

    # ... (código para calcular valores RGB promedio por celda, igual que antes)
    # Obtener ancho y alto
    width, height = imagen.size

    # Calcular número de filas y columnas
    num_rows = height // cell_size  # Mover aquí la definición de num_rows y num_cols
    num_cols = width // cell_size
    mean_r_total = 0
    mean_g_total = 0
    mean_b_total = 0

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

            # Calcular valores RGB promedio de la celda y acumular
            mean_r_total += np.mean(cell_array[:, :, 0])
            mean_g_total += np.mean(cell_array[:, :, 1])
            mean_b_total += np.mean(cell_array[:, :, 2])

    # Calcular valor RGB promedio de toda la pantalla
    mean_r = mean_r_total / (num_rows * num_cols)
    mean_g = mean_g_total / (num_rows * num_cols)
    mean_b = mean_b_total / (num_rows * num_cols)
    current_mean_rgb = np.array([mean_r, mean_g, mean_b])

    # Verificar si hay cambios bruscos (solo después de la primera iteración)
    if prev_mean_rgb is not None:
        diff = np.abs(current_mean_rgb - prev_mean_rgb)
        if np.any(diff > threshold) and not warning_shown:  # Verificar si se mostró la alerta
            show_warning()

    # Actualizar valor previo
    prev_mean_rgb = current_mean_rgb
    
    # Esperar para cumplir con la frecuencia de muestreo
    time.sleep(1 / sample_rate)

   
