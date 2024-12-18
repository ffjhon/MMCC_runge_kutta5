from machine import Pin, SPI
import time
import os
from ili9341 import Display, color565
from xglcd_font import XglcdFont

def mostrar_logo():   
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(15))
    display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7), rotation=180)

    display.draw_image('images/logo-mmcc.raw', 0, 0, 240, 320)
    time.sleep(5)
    display.cleanup()

def limpiar_pantalla():
    display.clear()

#---------------
mostrar_logo()
# Configurar pines para los botones
boton_codigo   = Pin(8, Pin.IN, Pin.PULL_DOWN)  # Botón para cambiar el código
boton_reinicio = Pin(16, Pin.IN, Pin.PULL_DOWN)  # Botón para reiniciar el script

# Variables para controlar el estado
estado_boton = 0  # Variable que alternará entre 0, 1 y 2
estado_anterior_codigo = False  # Para recordar el estado anterior del botón de código
estado_anterior_reinicio = False  # Para recordar el estado anterior del botón de reinicio

# Inicializa la pantalla LCD (ajusta la configuración según tu hardware)
spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(15))
display = Display(spi, dc=Pin(6), cs=Pin(17), rst=Pin(7), rotation=180)  # Ejemplo de configuración

# Limpiar la pantalla al inicio
#limpiar_pantalla()

# Mostrar el mensaje 'Semillero MMCC' con la fuente 'Broadway17x15'
#fuente = XglcdFont('fonts/Broadway17x15.c', 17, 15)  # Usar la fuente que especificaste
#display.draw_text(50, 150, "Semillero MMCC", fuente, color565(255, 255, 255), color565(0, 0, 0))
#time.sleep(3)
#display.show()  # Actualiza la pantalla para mostrar el texto
# Limpiar la pantalla para preparar la ejecución del primer script
#limpiar_pantalla()

# Ejecutar el primer script al iniciar
try:
    exec(open('MMCC_Euler.py').read())
    print("Ejecutando MMCC_Euler.py al inicio")
except OSError as e:
    print(f"Error al ejecutar MMCC_Euler.py al inicio: {e}")

while True:
    # Leer el estado actual del botón para cambiar de código
    estado_actual_codigo = boton_codigo.value()

    # Detectar el cambio de estado (flanco de subida)
    if estado_actual_codigo == 1 and estado_anterior_codigo == 0:  # Solo se cambia cuando el botón se presiona
        # Cambiar el valor de estado_boton de 0 a 1, de 1 a 2, de 2 a 0, etc.
        estado_boton = (estado_boton + 1) % 3
        print(f"Estado del botón de cambio de código: {estado_boton}")
        
        # Ejecutar el código correspondiente dependiendo de `estado_boton`
        if estado_boton == 0:
            try:
                exec(open('MMCC_Euler.py').read())
                print("Ejecutando MMCC_Euler.py")
            except OSError as e:
                print(f"Error al ejecutar MMCC_Euler.py: {e}")
        elif estado_boton == 1:
            try:
                exec(open('MMCC_RK5.py').read())
                print("Ejecutando MMCC_RK5.py")
            except OSError as e:
                print(f"Error al ejecutar MMCC_RK5.py: {e}")
        elif estado_boton == 2:
            try:
                exec(open('MMCC_EulerRK5.py').read())
                print("Ejecutando MMCC_EulerRK5.py")
            except OSError as e:
                print(f"Error al ejecutar MMCC_EulerRK5.py: {e}")
    
    # Leer el estado actual del botón para reiniciar el script
    estado_actual_reinicio = boton_reinicio.value()

    # Detectar el cambio de estado (flanco de subida) para el botón de reinicio
    if estado_actual_reinicio == 1 and estado_anterior_reinicio == 0:  # Solo se cambia cuando el botón se presiona
        print("Botón de reinicio presionado, reiniciando el script...")
        # Limpiar pantalla y reiniciar el script
        limpiar_pantalla()
        time.sleep(1)  # Esperar para asegurar que la pantalla se ha limpiado
        # Mostrar el logo de nuevo
        mostrar_logo()
        estado_boton = 0

        # Ejecutar el primer script al reiniciar
        try:
            # Aquí puedes llamar a tu script principal o usar `machine.reset()` para reiniciar el microcontrolador
            exec(open('MMCC_Euler.py').read())
            print("Ejecutando MMCC_Euler.py al reiniciar")
        except OSError as e:
            print(f"Error al ejecutar MMCC_Euler.py al reiniciar: {e}")
    
    # Actualizar los estados anteriores para la próxima lectura
    estado_anterior_codigo   = estado_actual_codigo
    estado_anterior_reinicio = estado_actual_reinicio
    
    time.sleep(0.1)  # Pausa pequeña para evitar lectura demasiado rápida
