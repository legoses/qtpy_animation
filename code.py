import busio
import board
import display
import time


#i2c = buso.I2C(board.SCL, board.SDA)


#while not i2c.try_lock():
#    pass


dispArr = [
    [1, 2],
    [2, 1],
    [4, 1],
    [2, 1],
    [1, 1],
    [3, 1],
]

#display = segdisplay.Display(dispArr)
#display.animate(True)

address = 0x70

i2c = busio.I2C(board.SCL, board.SDA)
display.begin(i2c, address)

display.write(dispArr[0])
display.write(dispArr[1])
display.write(dispArr[2])
display.write(dispArr[3])
display.show()

display.brightness(1)