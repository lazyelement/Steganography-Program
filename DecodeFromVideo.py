import base64
import cv2
import os.path
import shutil
import numpy as np
from subprocess import call,STDOUT

class Decode:
    
    def __init__(self, stegoObjPath, numOfBits):
        self.stegoObjPath = stegoObjPath
        self.numOfBits = numOfBits

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

    def frameExtraction(videoPath):
        # Create a temp folder if it does not exist
        if not os.path.exists("./tmp"):
            os.makedirs("tmp")
        tempFolder="./tmp"

        # Opens the video file using OpenCV library
        vidcap = cv2.VideoCapture(videoPath)
        count = 0
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        imgResolution = 0
        imgChannel = 0
        while True:
            # Read each frame from the video
            success, image = vidcap.read()
            if not success:
                # Return after all frames have been read
                return [count, imgResolution, imgChannel, fps]
            # Save each frame from the video into a temp folder
            cv2.imwrite(os.path.join(tempFolder, "{:d}.png".format(count)), image)
            count += 1
            imgResolution = image.shape[0] * image.shape[1]
            imgChannel = image.shape[2]

    # Method to show/decode the data hidden in the video
    def showData(self):
        # Extract the frames from the stego video and get the number of total frames, each frame's resolution and the channel for the frames (3 for RGB and 4 for RGBA)
        frameExtracted = Decode.frameExtraction(self.stegoObjPath)
        numOfFrames = frameExtracted[0]
        imgChannels = frameExtracted[2]

        decodedData = ""
        # Loop through each frame of the stego video
        for frame in range(numOfFrames):
            # Empty variable to store the binary data extracted from the image
            binaryData = ''

            
            # Stop decoding after we have reached the delimeter which is "#####"
            print('1')
            if decodedData[-5:] == "#####":
                    break

            print('Processing frame: ', frame+1)

            # Opens the current frame image using OpenCV library
            imgPath = os.path.abspath("./tmp/{:d}.png".format(frame))
            image = cv2.imread(imgPath)

            # Loop through each pixel in the current frame
            for values in image:
                for pixel in values:

                    if imgChannels == 3:
                        # convert RGB values to binary format
                        r, g, b = Decode.dataToBinary(pixel)
                        binaryData += r[-self.numOfBits:] #extracting data from the LSB of red pixel based on bits specified by user
                        binaryData += g[-self.numOfBits:] #extracting data from the LSB of green pixel based on bits specified by user
                        binaryData += b[-self.numOfBits:] #extracting data from the LSB of blue pixel based on bits specified by user
                    elif imgChannels == 4:
                        # convert RGBA values to binary format
                        r, g, b, a = Decode.dataToBinary(pixel)
                        binaryData += r[-self.numOfBits:] #extracting data from the LSB of red pixel based on bits specified by user
                        binaryData += g[-self.numOfBits:] #extracting data from the LSB of green pixel based on bits specified by user
                        binaryData += b[-self.numOfBits:] #extracting data from the LSB of blue pixel based on bits specified by user
                        binaryData += a[-self.numOfBits:] #extracting data from the LSB of black pixel based on bits specified by user
            
            print('2')
            # split the binary data to groups of 8
            allBytes = [binaryData[i: i+8] for i in range(0, len(binaryData), 8)]
            
            print('3')
            # convert from bits to characters
            for byte in allBytes:
                decodedData += chr(int(byte, 2))
                # Stop decoding after we have reached the delimeter which is "#####"
                # if "#####" in decodedData:
                #     break
                if decodedData[-5:] == "#####":
                    print('4')
                    break
            print('5')
        # Removes delimeter
        decodedData = decodedData[:-5]
        # Get the file extension and removes it
        fileExt = decodedData[-10:]
        decodedData = decodedData[:-10]
        # Remove padding from file extention
        fileExt = fileExt.replace("@", "")

        # Converts the hidden data back to a file from a Base64 format
        decodedData = base64.b64decode(eval(decodedData))

        # Write the decoded data back to a file and saves it
        decodedImgName = input("Filename to save as (Without file extension): ")
        with open(decodedImgName + fileExt, "wb") as outFile:
            outFile.write(decodedData)

        # Clears the temp folder
        if os.path.exists("./tmp"):
            shutil.rmtree("./tmp")

filename = input("Enter file name to decode: ")
filepath = os.path.join(os.getcwd(), filename)

numOfBits = int(input("Enter number of LSB to use: "))
de = Decode(filepath, numOfBits)
de.showData()

