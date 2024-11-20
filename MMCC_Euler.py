from machine import Pin, SPI
from ili9341 import Display, color565
from xglcd_font import XglcdFont
import math
import time

# Parámetros y condiciones iniciales (ajusta según tus necesidades)
h = 0.1
t = 0
Q = [0, 0]
N = 200  # Mayor número de iteraciones para una gráfica más detallada
cos_values = [math.cos(11 * (t * h)) for t in range(N)]  # Precomputar los valores de coseno

# Configuración de la pantalla
spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(15))
lcd = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7), rotation=180)

# Texto que se muestra en la pantalla TFT
fuente = XglcdFont('fonts/Broadway17x15.c', 17, 15)
lcd.draw_text(40, 290, 'Metodo de Euler', fuente, color565(255, 255, 255), color565(0, 0, 0))

# Función para calcular la derivada
def F(t, Q):
    return [Q[1], 550 * cos_values[int(t)] - 5 * Q[1] - 6 * Q[0]]

# Método de Euler y almacenamiento de resultados
euler = [0] * N  # Inicializar lista para los resultados de Euler

for i in range(1, N):
    Q_euler = [Q[0] + h * F(t, Q)[0], Q[1] + h * F(t, Q)[1]]
    euler[i] = Q_euler[0]
    Q = Q_euler
    t += h

# Encontrar los valores máximo y mínimo de Euler
max_euler = max(euler)
min_euler = min(euler)

# Escalar los valores de Euler para que se ajusten a la pantalla
scale = 230 / (max_euler - min_euler)

# Limpiar la pantalla (si el fondo es negro, no es necesario hacer nada)
# Si la pantalla no tiene un color de fondo negro, puedes usar el siguiente código:
# lcd.fill_rect(0, 0, 320, 240, color565(0, 0, 0))  # Fondo negro

# Dibujar los ejes
lcd.draw_line(0, 250, 230, 250, color565(200, 200, 200)) # Eje X (línea horizontal)
lcd.draw_line(0, 0, 0, 250, color565(255, 255, 255))  	 # Eje Y (línea vertical)

# Dibujar la gráfica de manera eficiente (usando líneas)
for i in range(1, N):
    x1 = (i - 1) * 2  # Ajuste de escala de X
    y1 = int(240 - (euler[i - 1] - min_euler) * scale)
    x2 = i * 2
    y2 = int(240 - (euler[i] - min_euler) * scale)
    lcd.draw_line(x1, y1, x2, y2, color565(0, 255, 255))  # Dibujar la línea Cian

# Mostrar la gráfica en la pantalla
time.sleep(5)

