import base64
import cv2
import os.path
import numpy as np

class Decode:
    
    def __init__(self, imgPath, noOfBits):
        self.imgPath = imgPath
        self.noOfBits = noOfBits

    # Method to convert data into binary format
    def dataToBinary(data):
        if type(data) == str:
            return ''.join([format(ord(i), "08b") for i in data])
        elif type(data) == bytes or type(data) == np.ndarray:
            return [format(i, "08b") for i in data]
        elif type(data) == int or type(data) == np.uint8:
            return format(data, "08b")
        else:
            # Input type not able to be changed to binary
            raise TypeError("Input type not supported")

    # Method to show/decode the data hidden in the image
    def showData(self):
        # Empty variable to store the binary data extracted from the image
        binaryData = ''

        # Opens the image to be decoded using cv2 library
        image = cv2.imread(self.imgPath)

        # Check the number of channels for the image (3 for RGB and 4 for RGBA)
        channels = image.shape[2]

        # Loop through each pixel in the image
        for values in image:
            for pixel in values:
                if channels == 3:
                    # convert RGB values to binary format
                    r, g, b = Decode.dataToBinary(pixel)
                    binaryData += r[-1] #extracting data from the least significant bit of red pixel
                    binaryData += g[-1] #extracting data from the least significant bit of green pixel
                    binaryData += b[-1] #extracting data from the least significant bit of blue pixel
                elif channels == 4:
                    # convert RGBA values to binary format
                    r, g, b, a = Decode.dataToBinary(pixel)
                    binaryData += r[-1] #extracting data from the least significant bit of red pixel
                    binaryData += g[-1] #extracting data from the least significant bit of green pixel
                    binaryData += b[-1] #extracting data from the least significant bit of blue pixel
                    binaryData += a[-1] #extracting data from the least significant bit of black pixel
        
        # split the binary data to groups of 8
        allBytes = [binaryData[i: i+8] for i in range(0, len(binaryData), 8)]

        # convert from bits to characters
        decodedData = ""
        for byte in allBytes:
            decodedData += chr(int(byte, 2))
            if decodedData[-5:] == "#####": #check if we have reached the delimeter which is "#####"
                break
            
        # Converts the hidden data back to an image file from a Base64 format
        decodedData = eval(decodedData[:-5])
        decodedArr = np.frombuffer(base64.b64decode(decodedData), dtype=np.uint8)
        decodedImg = cv2.imdecode(decodedArr, flags=cv2.IMREAD_COLOR)

        # Saves the decoded file
        decodedImgName = input("Filename to save as (Without file extension): ")
        cv2.imwrite(os.path.join(os.getcwd(), decodedImgName + '.png'), decodedImg)
        cv2.waitKey(0)

filename = input("Enter file name to decode: ")
filepath = os.path.join(os.getcwd(), filename)
de = Decode(filepath, 1)
de.showData()

