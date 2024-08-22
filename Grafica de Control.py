# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 21:21:17 2024

@author: gutierrm
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import os

# Obtener la ruta del directorio donde se encuentra el archivo Python
current_directory = os.path.dirname(os.path.abspath(__file__))
csv_filename = 'datos.csv'  # Cambia esto por el nombre de tu archivo CSV
csv_path = os.path.join(current_directory, csv_filename)

# Cargar los datos desde el archivo CSV
data = pd.read_csv(csv_path)

# Asumiendo que los datos relevantes están en una columna específica, por ejemplo, 'Mediciones'
data_column = 'Mediciones'  # Cambia esto al nombre real de tu columna
data_values = data[data_column].values

# Parámetros de la gráfica de control
mean = np.mean(data_values)
std_dev = np.std(data_values)
n = len(data_values)

# Límites de control
LCL = mean - 3*std_dev
UCL = mean + 3*std_dev
CL = mean

# Zonas para la gráfica
zone_a = [mean - 3*std_dev, mean - 2*std_dev, mean + 2*std_dev, mean + 3*std_dev]
zone_b = [mean - 2*std_dev, mean - 1*std_dev, mean + 1*std_dev, mean + 2*std_dev]
zone_c = [mean - 1*std_dev, mean, mean, mean + 1*std_dev]

# Curva de distribución normal
x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
pdf = norm.pdf(x, mean, std_dev)

# Gráfico de distribución normal
fig, (ax1, ax2) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [1, 3]}, figsize=(12, 5))
ax1.plot(pdf, x, color='#FF0000')  # Curva de distribución normal en rojo
# Eliminar sombreado amarillo
# ax1.fill_betweenx(x, 0, pdf, where=((x > zone_a[0]) & (x < zone_a[3])), color='yellow', alpha=0.5)
ax1.fill_betweenx(x, 0, pdf, where=((x > zone_b[0]) & (x < zone_b[3])), color='gray', alpha=0.5)  # Zona B en gris
ax1.fill_betweenx(x, 0, pdf, where=((x > zone_c[0]) & (x < zone_c[3])), color='lightgray', alpha=0.5)  # Zona C en gris claro
ax1.axhline(mean, color='blue', linestyle='--')
ax1.axhline(LCL, color='red', linestyle='--')
ax1.axhline(UCL, color='red', linestyle='--')
ax1.invert_xaxis()  # Invierte el eje x para poner los números a la izquierda

# Asegurar que los ejes y coincidan
ax1.set_ylim([min(LCL, min(data_values)), max(UCL, max(data_values))])

# Gráfico de control con marcadores
ax2.plot(data_values, marker='o', linestyle='-', color='#FF0000')  # Línea de tendencia en rojo con marcadores
ax2.axhline(mean, color='blue', linestyle='--', label='CL')
ax2.axhline(LCL, color='red', linestyle='--', label='LCL')
ax2.axhline(UCL, color='red', linestyle='--', label='UCL')
ax2.axhspan(zone_b[0], zone_b[1], facecolor='gray', alpha=0.3, label='Zona B')  # Zona B en gris
ax2.axhspan(zone_b[2], zone_b[3], facecolor='gray', alpha=0.3)
ax2.axhspan(zone_c[0], zone_c[1], facecolor='lightgray', alpha=0.5, label='Zona C')  # Zona C en gris claro
ax2.axhspan(zone_c[2], zone_c[3], facecolor='lightgray', alpha=0.5)

# Asegurar que los ejes y coincidan
ax2.set_ylim([min(LCL, min(data_values)), max(UCL, max(data_values))])

# Ajustes de los ejes
ax1.yaxis.tick_left()
ax1.yaxis.set_label_position("left")
ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")

# Etiquetas y título
ax1.set_xlabel('Densidad de probabilidad')
ax1.set_ylabel('Mediciones')
ax2.set_xlabel('Muestras')
ax2.set_ylabel('Mediciones')
plt.suptitle('Gráfica de Control con Zonas y Curva Normal')

plt.tight_layout()
plt.subplots_adjust(top=0.85, wspace=0.05)  # Ajuste del espacio entre gráficos
plt.show()
