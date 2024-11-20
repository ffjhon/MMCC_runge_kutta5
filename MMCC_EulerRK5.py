from machine import Pin, SPI
from ili9341 import Display, color565
from xglcd_font import XglcdFont
import math
import time

# Configuración de SPI y pines para el TFT ILI9341
spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(15))
display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7), rotation=180)

# Fuente para texto
fuente = XglcdFont('fonts/Broadway17x15.c', 17, 15)

# Parámetros y condiciones iniciales
h = 0.1  # Paso de tiempo
t = 0     # Tiempo inicial
Q = [0, 0]  # Condiciones iniciales
N = 21  # Número de iteraciones para Euler
N_RK5 = 21  # Número de iteraciones para RK5

# Método de Runge-Kutta de 5to orden (RK5)
def metodo_rk5():
    Q = [0, 0]  # Condiciones iniciales
    t = 0  # Tiempo inicial
    rk5 = [0] * N_RK5  # Inicializar lista para resultados de RK5

    for i in range(N_RK5):
        k1 = [h * x for x in F(t, Q)]
        k2 = [h * x for x in F(t + h/4, [Q[0] + k1[0]/4, Q[1] + k1[1]/4])]
        k3 = [h * x for x in F(t + h/4, [Q[0] + (k1[0] + k2[0])/8, Q[1] + (k1[1] + k2[1])/8])]
        k4 = [h * x for x in F(t + h/2, [Q[0] - k2[0]/2 + k3[0], Q[1] - k2[1]/2 + k3[1]])]
        k5 = [h * x for x in F(t + 3*h/4, [Q[0] + 3*k1[0]/16 + 9*k4[0]/16, Q[1] + 3*k1[1]/16 + 9*k4[1]/16])]
        k6 = [h * x for x in F(t + h, [Q[0] - 3*k1[0]/7 + 2*k2[0]/7 + 12*k3[0]/7 - 12*k4[0]/7 + 8*k5[0]/7,
                                      Q[1] - 3*k1[1]/7 + 2*k2[1]/7 + 12*k3[1]/7 - 12*k4[1]/7 + 8*k5[1]/7])]
        
        # Calcular la nueva posición Q utilizando el método RK5
        Q_RK5_nueva = [Q[0] + (1/90) * (7*k1[0] + 32*k3[0] + 12*k4[0] + 32*k5[0] + 7*k6[0]),
                       Q[1] + (1/90) * (7*k1[1] + 32*k3[1] + 12*k4[1] + 32*k5[1] + 7*k6[1])]
        rk5[i] = Q_RK5_nueva[0]  # Guardamos el valor de RK5

        # Actualizamos Q para la siguiente iteración
        Q = Q_RK5_nueva
        t += h  # Avanzamos en el tiempo

    return rk5

# Función para calcular la derivada
def F(t, Q):
    return [Q[1], 550 * math.cos(11 * t) - 5 * Q[1] - 6 * Q[0]]

# Método de Euler
def metodo_euler():
    Q = [0, 0]  # Condiciones iniciales
    t = 0  # Tiempo inicial
    euler = [0] * N  # Inicializar lista para los resultados de Euler

    for i in range(1, N):
        Q_euler = [Q[0] + h * F(t, Q)[0], Q[1] + h * F(t, Q)[1]]
        euler[i] = Q_euler[0]
        Q = Q_euler
        t += h

    return euler

# Mostrar el título en el display
# lcd.draw_text(40, 290, 'Metodo de Euler', fuente, color565(255, 255, 255), color565(0, 0, 0))
display.draw_text(50, 290, 'Euler vs RK5', fuente, color565(255, 255, 255), color565(0, 0, 0))

# Obtener los resultados
euler = metodo_euler()
rk5 = metodo_rk5()

# Encontrar los valores máximo y mínimo de ambos métodos para escalar las gráficas
max_euler = max(euler)
min_euler = min(euler)
max_rk5 = max(rk5)
min_rk5 = min(rk5)

# Escalar los valores de ambos métodos para que se ajusten a la pantalla
scale_euler = 230 / (max_euler - min_euler)
scale_rk5 = 230 / (max_rk5 - min_rk5)

# Limpiar la pantalla
#display.draw_fill_rect(0, 0, 320, 240, color565(0, 0, 0))  # Fondo negro

# Dibujar los ejes
display.draw_line(0, 250, 230, 250, color565(200, 200, 200)) # Eje X (línea horizontal)
display.draw_line(0, 0, 0, 250,     color565(255, 255, 255))  	 # Eje Y (línea vertical)

# Dibujar las gráficas de ambos métodos en la pantalla (usando líneas)
for i in range(1, N):
    # Método de Euler (color azul)
    x1_euler = (i - 1) * 15
    y1_euler = int(240 - (euler[i - 1] - min_euler) * scale_euler)
    x2_euler = i * 15
    y2_euler = int(240 - (euler[i] - min_euler) * scale_euler)
    display.draw_line(x1_euler, y1_euler, x2_euler, y2_euler, color565(0, 255, 255))  # Línea Cian

    # Método de RK5 (color rojo)
    x1_rk5 = (i - 1) * 15
    y1_rk5 = int(240 - (rk5[i - 1] - min_rk5) * scale_rk5)
    x2_rk5 = i * 15
    y2_rk5 = int(240 - (rk5[i] - min_rk5) * scale_rk5)
    display.draw_line(x1_rk5, y1_rk5, x2_rk5, y2_rk5, color565(255, 0, 0))  # Línea roja

# Mantener la visualización por un tiempo
time.sleep(10)
