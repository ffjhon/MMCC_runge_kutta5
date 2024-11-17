import machine
import time
import numpy as np
from ili9341 import ILI9341
import tft_config  # Asegúrate de tener la configuración de la pantalla TFT

# Condiciones iniciales
h = 0.1; t = 0; 
Q = np.array([0, 0])  # Condiciones iniciales
N = 21  # Número de iteraciones

# Inicializar arrays para almacenar resultados
v_real = np.zeros(N)
euler  = np.zeros(N)
euler_error = np.zeros(N)
rk5 = np.zeros(N)
rk5_error = np.zeros(N)

# Configurar la pantalla
spi = machine.SPI(1, baudrate=40000000, polarity=0, phase=0)
cs  = machine.Pin(15, machine.Pin.OUT)  # Pin de Chip Select
dc  = machine.Pin(2, machine.Pin.OUT)   # Pin de Data/Command
rst = machine.Pin(4, machine.Pin.OUT)   # Pin de Reset
lcd = ILI9341(spi, cs, dc, rst)

# Función de la derivada
def F(t, Q):
    return np.array([Q[1], 550 * np.cos(11 * t) - 5 * Q[1] - 6 * Q[0]])

for i in range(N):
    j = i-1
    
    # Método de Euler
    Q_euler = Q + h*F(t, Q)
    euler[i] = Q_euler[0]  # Guardamos el resultado del método de Euler

    # Método de Runge-Kutta de 5to orden (RK5)
    k1 = h * F(t, Q)
    k2 = h * F(t + h / 4, Q + k1 / 4)
    k3 = h * F(t + h / 4, Q + k1 / 8 + k2 / 8)
    k4 = h * F(t + h / 2, Q - k2 / 2 + k3)
    k5 = h * F(t + 3 * h / 4, Q + 3 * k1 / 16 + 9 * k4 / 16)
    k6 = h * F(t + h, Q - 3 * k1 / 7 + 2 * k2 / 7 + 12 * k3 / 7 - 12 * k4 / 7 + 8 * k5 / 7)
    
    Q_RK5_nueva = Q + (1 / 90) * (7 * k1 + 32 * k3 + 12 * k4 + 32 * k5 + 7 * k6)
    rk5[i] = Q_RK5_nueva[0]  # Guardamos el valor de RK5

    # Solución analítica (función exacta)
    #analitica = (-253 / 65) * np.cos(11 * t) + (121 / 65) * np.sin(11 * t) - (44 / 5) * np.exp(-2 * t) + (165 / 13) * np.exp(-3 * t)
    
    # Error de Euler y RK5 con respecto a la solución analítica
    euler_error[j] = abs(euler[j] - analitica)
    rk5_error[j]   = abs(rk5[j] - analitica)
    v_real[j]      = analitica
    
    # Actualizamos Q para la siguiente iteración
    Q = Q_RK5_nueva
    t += h  # Avanzamos en el tiempo

# Mostrar los resultados en la pantalla
lcd.fill(ILI9341.WHITE)

# Mostrar resultados de Euler y RK5
for i in range(N):
    x_pos = i * 10  # Escalar las posiciones de x para que quepan en la pantalla
    lcd.pixel(x_pos, int(240 - euler[i]*10), ILI9341.BLUE)   # Muestra Euler
    lcd.pixel(x_pos, int(240 - rk5[i]*10), ILI9341.RED)      # Muestra RK5

# Incluir un mensaje de texto
lcd.text("Euler y RK5", 10, 10, ILI9341.BLACK)

# Mostrar los errores (solo para la primera parte de los errores)
for i in range(min(N, 160)):
    lcd.pixel(i, int(240 - euler_error[i] * 20), ILI9341.GREEN)  # Error de Euler

# Puedes añadir más información o gráficos según sea necesario

# Esperar un poco antes de finalizar
time.sleep(5)
