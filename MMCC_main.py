from machine import Pin, SPI
import time, os
from ili9341 import Display, color565
from xglcd_font import XglcdFont

# Verificar los archivos disponibles
print(os.listdir())

# Función para limpiar la pantalla
def limpiar_pantalla():
    display.clear()  # Limpiar la pantalla utilizando el método 'clear'

# Configurar pines
boton = Pin(8, Pin.IN, Pin.PULL_DOWN)  # Ajusta el número de pin según tu conexión

# Variables para controlar el estado
estado_boton = 0  # Variable que alternará entre 0, 1 y 2
estado_anterior = False  # Para recordar el estado anterior del botón

# Inicializa la pantalla LCD (ajusta la configuración según tu hardware)
spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(15))
display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7), rotation=180)  # Ejemplo de configuración

# Limpiar la pantalla al inicio
limpiar_pantalla()

# Cargar la fuente 'Broadway17x15' (asegurarse de que esté en el directorio correcto)
fuente = XglcdFont('fonts/Broadway17x15.c', 17, 15)  # Usar la fuente que especificaste

# Mostrar el mensaje 'Semillero MMCC' con la fuente 'Broadway17x15'
display.draw_text(50, 150, "Semillero MMCC", fuente, color565(255, 255, 255), color565(0, 0, 0))
#display.show()  # Actualiza la pantalla para mostrar el texto

# Esperar 2 segundos antes de continuar
time.sleep(3)

# Limpiar la pantalla para preparar la ejecución del primer script
limpiar_pantalla()

# Ejecutar el primer script al iniciar
try:
    exec(open('MMCC_Euler.py').read())
    print("Ejecutando MMCC_Euler.py al inicio")
except OSError as e:
    print(f"Error al ejecutar MMCC_Euler.py al inicio: {e}")

while True:
    # Leer el estado actual del botón
    estado_actual = boton.value()

    # Detectar el cambio de estado (flanco de subida)
    if estado_actual == 1 and estado_anterior == 0:  # Solo se cambia cuando el botón se presiona
        # Cambiar el valor de estado_boton de 0 a 1, de 1 a 2, de 2 a 0, etc.
        estado_boton = (estado_boton + 1) % 3
        print(f"Estado del botón: {estado_boton}")
        
        # Ejecutar el código correspondiente dependiendo de `estado_boton`
        if estado_boton == 0:
            try:
                # Ejecutar MMCC_Euler.py
                exec(open('MMCC_Euler.py').read())
                print("Ejecutando MMCC_Euler.py")
            except OSError as e:
                print(f"Error al ejecutar MMCC_Euler.py: {e}")
        elif estado_boton == 1:
            try:
                # Ejecutar MMCC_RK5.py
                exec(open('MMCC_RK5.py').read())
                print("Ejecutando MMCC_RK5.py")
            except OSError as e:
                print(f"Error al ejecutar MMCC_RK5.py: {e}")
        elif estado_boton == 2:
            try:
                # Ejecutar MMCC_EulerRK5.py
                exec(open('MMCC_EulerRK5.py').read())
                print("Ejecutando MMCC_EulerRK5.py")
            except OSError as e:
                print(f"Error al ejecutar MMCC_EulerRK5.py: {e}")
    
    # Actualizar el estado anterior para la próxima lectura
    estado_anterior = estado_actual
    
    time.sleep(0.1)  # Pausa pequeña para evitar lectura demasiado rápida
