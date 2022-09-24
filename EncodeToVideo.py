import base64
import cv2
import os.path
import shutil
import numpy as np
from subprocess import call,STDOUT

class Encode:
    def __init__(self, coverVidFile, payloadFile, numOfBits):
        coverPath = os.path.join(os.getcwd(), coverVidFile)
        payloadPath = os.path.join(os.getcwd(), payloadFile)
        self.coverVidPath = coverPath
        self.payloadPath = payloadPath
        self.numOfBits = numOfBits


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

    # Method to hide/encode the encrypted binary data into the cover object
    def hideData(self):
        # Opens the payload object and encodes it into a Base64 format
        payloadB64 = ''
        with open(self.payloadPath, "rb") as payload:
            payloadB64 = base64.b64encode(payload.read())

        # Find extension of cover video and payload object
        coverExt = os.path.splitext(self.coverVidPath)[1]
        payloadExt = os.path.splitext(self.payloadPath)[1]

        # Add padding to file extention untill there is 10 characters
        while len(payloadExt) < 10:
            payloadExt += '@'

        # Extract the frames from the cover video
        frameExtracted = Encode.frameExtraction(self.coverVidPath)

        # Get the number of total frames, each frame's resolution, the channel for the frames (3 for RGB and 4 for RGBA) and the fps of the video
        numOfFrames = frameExtracted[0]
        imgResolution = frameExtracted[1]
        imgChannels = frameExtracted[2]
        fps = frameExtracted[3]

        # Extract the audio from the cover video
        call(["ffmpeg", "-i",self.coverVidPath, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

        # Calculate the maximum bytes that can be encoded for the cover video
        maxBytes = numOfFrames * ((imgResolution * self.numOfBits * 3) // 8)
        print("Maximum bytes to encode:", maxBytes)

        # Converts the encoded Base64 payload into a string and adds the file extention and the delimeter to indicate the end of the file
        payloadEncode = str(payloadB64) + payloadExt + '#####'

        # Check if the number of bytes of the payload object to encode is less than the maximum bytes in the cover video
        print('Payload size: ', len(payloadEncode))
        if len(payloadEncode) > maxBytes:
            raise ValueError("Error encountered insufficient bytes, need bigger video or less data !!")

        # Converts the encoded payload string to binary format
        dataToHideBin = Encode.dataToBinary(payloadEncode)

        # Get the length of the encoded payload binary
        dataLen = len(dataToHideBin)

        # setting a local variable to point to the binary value to encode in each iteration
        dataIndex = 0

        # Loop through frame of the cover video
        for frame in range(numOfFrames):
            # Break the loop if all the data have been hidden
            if (dataIndex >= dataLen):
                break
            
            # Opens the current frame image using OpenCV library
            imgPath = os.path.abspath("./tmp/{:d}.png".format(frame))
            image = cv2.imread(imgPath)

            print('Hiding in frame: ', frame+1)
            # Loop through each pixel in the current frame
            for values in image:
                for pixel in values:
                    r = 0
                    g = 0
                    b = 0
                    a = 0
                    
                    if imgChannels == 3:
                        # convert RGB values to binary format
                        r, g, b = Encode.dataToBinary(pixel)
                    elif imgChannels == 4:
                        # convert RGBA values to binary format
                        r, g, b, a = Encode.dataToBinary(pixel)

                    # modify the least significant bit only if there is still data to store
                    if dataIndex < dataLen:
                        tempBin = ''
                        # Remove the last few digits of the red pixel binary based on the number of LSB used
                        r = r[:-self.numOfBits]
                        # Loop and store the data to hide into a temp variable
                        for x in range(self.numOfBits):
                            tempBin += dataToHideBin[dataIndex]
                            dataIndex += 1
                            # Break the loop if all the data have been hidden
                            if dataIndex == dataLen:
                                break
                        # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
                        if len(tempBin) < self.numOfBits:
                            tempBin = tempBin.ljust(self.numOfBits, '0')
                        # Adds the temp binary to the pixel binary and change it into an integer and assign it to the pixel array
                        pixel[0] = int(r + tempBin, 2)
                    if dataIndex < dataLen:
                        tempBin = ''
                        # Remove the last few digits of the green pixel binary based on the number of LSB used
                        g = g[:-self.numOfBits]
                        # Loop and store the data to hide into a temp variable
                        for x in range(self.numOfBits):
                            tempBin += dataToHideBin[dataIndex]
                            dataIndex += 1
                            # Break the loop if all the data have been hidden
                            if dataIndex == dataLen:
                                break
                        # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
                        if len(tempBin) < self.numOfBits:
                            tempBin = tempBin.ljust(self.numOfBits, '0')
                        # Adds the temp binary to the pixel binary and change it into an integer and assign it to the pixel array
                        pixel[1] = int(g + tempBin, 2)
                    if dataIndex < dataLen:
                        tempBin = ''
                        # Remove the last few digits of the blue pixel binary based on the number of LSB used
                        b = b[:-self.numOfBits]
                        # Loop and store the data to hide into a temp variable
                        for x in range(self.numOfBits):
                            tempBin += dataToHideBin[dataIndex]
                            dataIndex += 1
                            # Break the loop if all the data have been hidden
                            if dataIndex == dataLen:
                                break
                        # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
                        if len(tempBin) < self.numOfBits:
                            tempBin = tempBin.ljust(self.numOfBits, '0')
                        # Adds the temp binary to the pixel binary and change it into an integer and assign it to the pixel array
                        pixel[2] = int(b + tempBin, 2)
                    if (dataIndex < dataLen) and (imgChannels == 4): # If channel is 4 (RGBA image)
                        tempBin = ''
                        # Remove the last few digits of the black pixel binary based on the number of LSB used
                        a = a[:-self.numOfBits]
                        # Loop and store the data to hide into a temp variable
                        for x in range(self.numOfBits):
                            tempBin += dataToHideBin[dataIndex]
                            dataIndex += 1
                            # Break the loop if all the data have been hidden
                            if dataIndex == dataLen:
                                break
                        # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
                        if len(tempBin) < self.numOfBits:
                            tempBin = tempBin.ljust(self.numOfBits, '0')
                        # Adds the temp binary to the pixel binary and change it into an integer and assign it to the pixel array
                        pixel[3] = int(a + tempBin, 2)

                    # Break the loop if all the data have been hidden
                    if dataIndex >= dataLen:
                        break

            # Save the edited frame
            cv2.imwrite(os.path.join(os.getcwd(), "tmp/{:d}.png".format(frame)), image)

        # Write the output stego object to a temp video file 
        call(["ffmpeg", "-framerate", str(fps), "-i", "tmp/%d.png", "-vcodec", "png", "tmp/temp.avi", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        
        # Puts the audio back to the temp video file
        call(["ffmpeg", "-i", "tmp/temp.avi", "-i", "tmp/audio.mp3", "-codec", "copy", "tmp/outputVid.avi", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)

        # Change the temp video file into a format that can be played
        stegoObjName = input("Filename to save as (Without file extension): ")
        call(["ffmpeg", "-i", "tmp/outputVid.avi", "-f", "avi", "-c:v", "rawvideo", "-pix_fmt", "rgb32", stegoObjName+coverExt], stdout=open(os.devnull, "w"), stderr=STDOUT)

        # Clears the temp folder
        if os.path.exists("./tmp"):
            shutil.rmtree("./tmp")

coverFile = input("Enter cover video file name: ")
payloadFile = input("Enter payload object file name: ")
numOfBits = int(input("Enter number of LSB to use: "))

en = Encode(coverFile, payloadFile, numOfBits)
en.hideData()