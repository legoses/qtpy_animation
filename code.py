import board
from adafruit_ht16k33.segments import Seg14x4
import animation
import time


#Contains segment number to light up, and grid to display on
stepsTrail = [
    [7, 1],
    [6, 1],
    [0, 1],
    [1, 1],
    [3, 1],
    [4, 1],
    [4, 2], #start of next grid
    [5, 2],
    [0, 2],
    [1, 2],
    [2, 2],
    [7, 2],
    [7, 3], #start of next grid
    [6, 3],
    [0, 3],
    [1, 3],
    [3, 3],
    [4, 3],
    [4, 4], #start of next grid
    [5, 4],
    [0, 4],
    [1, 4],
    [2, 4],
    [7, 4],
    [6, 4], #Start reverse
    [0, 4],
    [1, 4],
    [3, 4],
    [4, 3], #start of next grid
    [3, 3],
    [1, 3],
    [0, 3],
    [6, 3],
    [7, 3],
    [7, 2], #start of next grid
    [2, 2],
    [1, 2],
    [0, 2],
    [5, 2],
    [4, 2],
    [4, 1], #start of next grid
    [3, 1],
    [2, 1],
]

i2c = board.STEMMA_I2C()
address:int = 0x72

display = Seg14x4(i2c, address=(address))
display.brightness = 0.2

#test = animation.DisplayPattern(stepsTrail, address, i2c)
#test.speed = .5
#test.start(True)


test = animation.DisplayPattern(stepsTrail, address, i2c)
test.start(True)