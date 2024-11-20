#import picoexplorer as display
import picodisplay as display
#Screen essentials
width = display.get_width()
height = display.get_height()
display_buffer = bytearray(width * height * 2)
display.init(display_buffer)