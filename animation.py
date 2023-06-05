import time


class DisplayPattern:
    def __init__(self, dispArr, address, i2c, speed=0.1, trail = 2):
        self.__dispArr = dispArr
        self.__address = address
        self.__speed = speed
        self.__gridAddr: int = [0x00, 0x02, 0x04, 0x06]
        self.__i2c = i2c
        self.__trail = trail


    def __checkArr(self):
        for i in range(len(self.__dispArr)):
            if len(self.__dispArr[i]) != 2:
                raise ValueError(f'Line {i+1} is missing a value')
            else:
                if (self.__dispArr[i][0] > 7) or (self.__dispArr[i][0] < 0):
                    raise ValueError(f"Segment value in row {i+1} is incorrect. Must be between 0 and 7.")
                if (self.__dispArr[i][1] > 4) or (self.__dispArr[i][1] < 0):
                    raise ValueError(f'Grid number in row {i+1} is in correct. Must be between 0 and 4')


    def __displayTwoSeg(self, curPos) -> int:
        byteArr = ["0", "0", "0", "0", "0", "0", "0", "0"]

        if curPos == 0:
            byteArr[self.__dispArr[curPos][0]] = "1"
        else:
            byteArr[self.__dispArr[curPos][0]] = "1"
            byteArr[self.__dispArr[curPos-1][0]] = "1"

        byteArrStr = "".join(byteArr)
        byteStr = "0b" + byteArrStr
        return int(byteStr)

    
    def __dispOneSeg(self, curPos) -> int:
        byteArr = ["0", "0", "0", "0", "0", "0", "0", "0"]
        byteArr[self.__dispArr[curPos][0]] = "1"

        byteArrStr = "".join(byteArr)
        byteStr = "0b" + byteArrStr
        return int(byteStr)



    def clearPrevGrid(self, prevGrid) -> void:
        prevGridIndex = self.__gridAddr[prevGrid-1]
        self.__i2c.writeto(self.__address, bytearray((prevGridIndex, 0b00000000, 0b00000000)))


    @property
    def speed(self):
        return self.__speed


    @speed.setter
    def speed(self, value):
        if value <= 0:
            raise ValueError("Speed must be greater than 0")


    @property
    def segmentTrail(self):
        return self.__trail

    @segmentTrail.setter
    def segmentTrail(self, setTrail):
        if (setTrail > 0) and (setTrail < 8):
            self.__trail = setTrail
        else:
            raise ValueError("Trail must be greater than 0 and less than 8")




    def start(self, loop):
        self.__checkArr()
        writeBuffer = []
        
        self.__i2c.try_lock()
        #self.clearDisplay()

        #it seems like python is coverting binary bits to text. 01000000 is being converted to @ and causing issues when trying to write to the display
        while True:
            for i in range(len(self.__dispArr)):
                #Get the grid the user selected
                #User will choose a number between 1 and 4. Subtract 1 to get the array index
                gridNum = self.__gridAddr[self.__dispArr[i][1] - 1]
                prevGridNum = self.__gridAddr[self.__dispArr[i-1][1] - 1]

                #Get the byte to switch on segment
                if gridNum == prevGridNum:
                    byte = self.__displayTwoSeg(i)
                    byteArray = bytearray((gridNum, byte, 0b00000000))
                    self.__i2c.writeto(self.__address, byteArray)
                else:
                    for j in range(self.__trail):
                        currentGrid = self.__dispOneSeg(i)
                        oldGrid = self.__dispOneSeg(i-1)

                        print(currentGrid)

                        currentByte = bytearray((gridNum, currentGrid, 0b00000000))
                        oldByte = bytearray((prevGridNum, oldGrid, 0b00000000))

                        self.__i2c.writeto(self.__address, currentByte)
                        self.__i2c.writeto(self.__address, oldByte)

                        i += 1




                

                

                #time.sleep(self.__speed)
                time.sleep(1)

            if loop == False:
                self.__i2c.unlock()
                return