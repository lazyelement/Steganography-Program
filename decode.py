#get file
#change file to binary
#get lsb

import cv2, numpy as np


class Decode:
    def __init__ (self, data, lsb):
        self.data = data
        self.lsb = lsb

    def dataType(self, data):
        pass

    # Converting data to binary
    def convertingDataToBinary (self, data):
        # Convert data to binary format as string
        if isinstance(data, str):
            return ''.join([ format(ord(i), "08b") for i in data ])
        elif isinstance(data, bytes) or isinstance(data, np.ndarray):
            return [ format(i, "08b") for i in data ]
        elif isinstance(data, int) or isinstance(data, np.uint8):
            return format(data, "08b")
        else:
            raise TypeError("Type not supported.")

    # Split Binary data to 8 bits
    def splitBinary(self):
        binary_data = ""
        for row in data:
            for pixel in row:
                r, g, b = self.convertingDataToBinary(pixel)
                binary_data += r[-1]
                binary_data += g[-1]
                binary_data += b[-1]
        # split by 8-bits
        all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
        print(all_bytes)
    
    
data = cv2.imread("catTest.jpeg")
test = Decode(data, 1)
test.splitBinary()




