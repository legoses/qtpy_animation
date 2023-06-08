import board
from adafruit_ht16k33.segments import Seg14x4
import animation
import time


#Contains segment number to light up, and grid to display on
stepsTrail = [
    [8, 0, 1],
    [7, 3, 1],
    [1, 3, 1],
    [2, 3, 1],
    [4, 3, 1],
    [5, 3, 1],
    [5, 3, 2], #start of next grid
    [6, 3, 2],
    [1, 3, 2],
    [2, 3, 2],
    [3, 0, 2],
    [8, 0, 2],
    [8, 0, 3], #start of next grid
    [7, 0, 3],
    [1, 0, 3],
    [2, 0, 3],
    [4, 0, 3],
    [5, 0, 3],
    [5, 0, 4], #start of next grid
    [6, 0, 4],
    [1, 0, 4],
    [2, 0, 4],
    [3, 0, 4],
    [8, 0, 4],
    [7, 0, 4], #Start reverse
    [1, 0, 4],
    [2, 0, 4],
    [4, 0, 4],
    [5, 0, 3], #start of next grid
    [4, 0, 3],
    [2, 0, 3],
    [1, 0, 3],
    [7, 0, 3],
    [8, 0, 3],
    [8, 0, 2], #start of next grid
    [3, 0, 2],
    [2, 0, 2],
    [1, 0, 2],
    [6, 0, 2],
    [3, 0, 2],
    [5, 0, 1], #start of next grid
    [4, 0, 1],
    [3, 0, 1],
]

i2c = board.STEMMA_I2C()
address:int = 0x72

display = Seg14x4(i2c, address=(address))
display.brightness = 0.2

#test = animation.DisplayPattern(stepsTrail, address, i2c)

#test.start(True)


test = animation.DisplayPattern(stepsTrail, address, i2c)
test.speed = .2
test.segmentTrail = 2
test.start(False)