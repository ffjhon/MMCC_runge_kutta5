"""Generic ESP32 with ST7789 240x320 display"""

from machine import Pin, SPI
import st7789

TFA = 0
BFA = 0

def config(rotation=0, buffer_size=0, options=0):
    return st7789.ST7789(
        SPI(1, baudrate=10000000, sck=Pin(14), mosi=Pin(15)),
        240,
        320,
        reset=Pin(7, Pin.OUT),
        cs=Pin(5, Pin.OUT),
        dc=Pin(4, Pin.OUT),
        backlight=Pin(15, Pin.OUT),
        rotation=rotation,
        options=options,
        buffer_size=buffer_size)
