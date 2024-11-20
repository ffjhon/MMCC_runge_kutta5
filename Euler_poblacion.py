from machine import Pin, SPI
from ili9341 import Display, color565
from xglcd_font import XglcdFont
import math

# Configuración del SPI y del display
spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(15))
display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7), rotation=180)

y0 = 100 # Condición inicial (población inicial de bacterias)
h = 0.1 # Tamaño del paso (en años)
t_final = 4 # Tiempo final (en años)

# Inicialización de variables
t = [i * h for i in range(int(t_final / h) + 1)]  # Vector de tiempo
y = [0] * len(t)  # Vector para almacenar los valores de y
y[0] = y0  # Condición inicial

# Método de Euler
for n in range(len(t) - 1):
    # Aplicación de la ecuación diferencial: dy/dt = y - t[n]**2 + 1
    f = y[n] - t[n]**2 + 1
    # Actualización del valor de y usando el método de Euler
    y[n + 1] = y[n] + h * f

# Visualización en el display TFT
width, height = 239, 260 # Tamaño de grafico
maxy = y[-1] # Poblacion maxima

# Texto que se muestra en la pantalla TFT
broadway = XglcdFont('fonts/Broadway17x15.c', 17, 15)
display.draw_text(40, 290, 'Metodo de Euler', broadway, color565(255, 255, 255), color565(0, 0, 0))

for i in range(len(t)):
    # Posicion X para pixeles TFT
    x = int((t[i] * (width//t_final)))
    # Posicion Y para pixeles TFT 
    y_pos = int(height-(y[i]* (height/maxy)))
    
    # Imprimir datos del proceso
    print(f"Tiempo: {t[i]:.1f} años, Población de Bacterias: {y[i]:.2f}, xTFT: {x:.3f}, yTFT: {y_pos:.4f}")
    
    if 0 <= x <= width and 0 <= y_pos <= height:
        display.draw_pixel(x, y_pos,color565(255, 255, 255))  # Dibujar el punto