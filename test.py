from machine import Pin, SPI
import time
import ili9341  # Asegúrate de tener la librería correcta instalada

# Configuración de SPI con los pines especificados
spi = SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(15))

# Configuración de los pines para la pantalla TFT ILI9341
cs = Pin(17, Pin.OUT)    # Chip Select
dc = Pin(6, Pin.OUT)     # Data/Command
rst = Pin(7, Pin.OUT)    # Reset

# Inicializar la pantalla TFT ILI9341
lcd = ili9341.ILI9341(spi, cs=cs, dc=dc, rst=rst)

# Rellenar la pantalla de blanco
lcd.fill(ili9341.color565(255, 255, 255))

# Espera para que puedas ver el color blanco en la pantalla
time.sleep(2)

# Mostrar texto en la pantalla
lcd.text("Pantalla Test", 50, 50, ili9341.color565(0, 0, 0))  # Texto en color negro
lcd.text("Raspberry Pi Pico W", 50, 80, ili9341.color565(0, 0, 0))  # Texto en color negro
