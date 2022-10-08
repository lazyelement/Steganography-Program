import base64
import cv2
import os.path
import numpy as np

class Encode:
    def __init__(self, coverImgPath, payloadPath, noOfBits):
        self.coverImgPath = coverImgPath
        self.payloadPath = payloadPath
        self.noOfBits = noOfBits


    # # checking if the image exists on given path
    # def is_image_path_valid(self):
    #     if os.path.exists(self.image_path):
    #         return True
    #     return False

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

    # Method to hide/encode the encrypted binary data into the image
    def hideData(self):
        # Opens the cover image and payload image using cv2 library
        coverImg = cv2.imread(self.coverImgPath)
        payloadImg = cv2.imread(self.payloadPath)
        
        # Encode the payload image into a Base64 format
        payloadExt = os.path.splitext(self.payloadPath)[1] # Find extension of image
        _, payloadArr = cv2.imencode(payloadExt, payloadImg)
        payloadB64 = base64.b64encode(payloadArr.tobytes())

        # Calculate the maximum bytes that can be encoded for the cover image
        maxBytes = coverImg.shape[0] * coverImg.shape[1] * 3 // 8
        print("Maximum bytes to encode:", maxBytes)

        # Check if the number of bytes of the payload image to encode is less than the maximum bytes in the cover image
        print('Payload size: ', payloadImg.size)
        if payloadImg.size > maxBytes:
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data !!")

        # Check the number of channels for the image (3 for RGB and 4 for RGBA)
        channels = coverImg.shape[2]

        # Converts the encoded Base64 format into a string and add a delimeter to indicate the end of the file
        payloadEncode = str(payloadB64) + '#####'

        # Converts the encoded payload string to binary format
        dataToHideBin = Encode.dataToBinary(payloadEncode)

        # Get the length of the encoded payload binary
        dataLen = len(dataToHideBin)

        # setting a local variable to point to the binary value to encode in each iteration
        dataIndex = 0
        # Loop through each pixel in the cover image
        for values in coverImg:
            for pixel in values:
                r = 0
                g = 0
                b = 0
                a = 0
                
                if channels == 3:
                    # convert RGB values to binary format
                    r, g, b = Encode.dataToBinary(pixel)
                elif channels == 4:
                    # convert RGBA values to binary format
                    r, g, b, a = Encode.dataToBinary(pixel)

                # modify the least significant bit only if there is still data to store
                if dataIndex < dataLen:
                    # hide the data into least significant bit of red pixel
                    pixel[0] = int(r[:-1] + dataToHideBin[dataIndex], 2)
                    dataIndex += 1
                if dataIndex < dataLen:
                    # hide the data into least significant bit of green pixel
                    pixel[1] = int(g[:-1] + dataToHideBin[dataIndex], 2)
                    dataIndex += 1
                if dataIndex < dataLen:
                    # hide the data into least significant bit of blue pixel
                    pixel[2] = int(b[:-1] + dataToHideBin[dataIndex], 2)
                    dataIndex += 1
                if (dataIndex < dataLen) and (channels == 4): # If channel is 4 (RGBA image)
                    # hide the data into least significant bit of black pixel
                    pixel[3] = int(a[:-1] + dataToHideBin[dataIndex], 2)
                    dataIndex += 1
                # Break out of the loop once data have finished encoding
                if dataIndex >= dataLen:
                    break
        
        # Write the output stegoimage to a file
        stegoImgName = input("Filename to save as (Without file extension): ")
        cv2.imwrite(os.path.join(os.getcwd(), stegoImgName + '.png'), coverImg)
        cv2.waitKey(0)


coverFile = input("Enter cover image file name: ")
payloadFile = input("Enter payload image file name: ")
coverPath = os.path.join(os.getcwd(), coverFile)
payloadPath = os.path.join(os.getcwd(), payloadFile)

en = Encode(coverPath, payloadPath, 1)
en.hideData()

