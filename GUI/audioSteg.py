#This program is for encoding and decoding audio files
#It works for .wav/mp3 files
#The payload has to be in .txt/.xlsx/.xls/.docx format

import os
import numpy as np
import wave
import base64
import shutil
from subprocess import call,STDOUT
from os.path import join

# convert data to binary
def dataToBin(data):
    if type(data) == str:
        return ''.join([format(ord(i), "08b") for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [format(i, "08b") for i in data]
    elif type(data) == int or type(data) == np.uint8:
        return format(data, "08b")
    else:
        # Input type not able to be changed to binary
        raise TypeError("Input type not supported")

def encoding_audio(payload,audio_file,LSB_bit,isPath):
    # Check if payload is a file
    if isPath:
        # Get path of payload file
        payloadPath = os.path.join(os.getcwd(), payload)

        # Find extension of payload file
        payloadExt = os.path.splitext(payloadPath)[1]

        # Add padding to file extention untill there is 10 characters
        while len(payloadExt) < 10:
            payloadExt += '@'

        # Opens the payload file and encodes it into a Base64 format
        payloadB64 = ''
        with open(payloadPath, "rb") as payload:
            payloadB64 = base64.b64encode(payload.read())

        # Converts the encoded Base64 payload into a string and adds the file extention and the delimeter to indicate the end of the file
        payloadEncode = str(payloadB64) + payloadExt + "#####"
    # If payload is a string
    else:
        payloadString = payload
        # Encodes the payload into a Base64 format
        payloadB64 = base64.b64encode(payloadString.encode('utf-8'))
        # Converts the encoded Base64 payload into a string and adds the delimeter to indicate the end of the file
        payloadEncode = str(payloadB64) + '$' + '#####'

    # Get path of cover audio
    audioPath = os.path.join(os.getcwd(), audio_file)
    
    # Find extension of cover audio
    audioExt = os.path.splitext(audioPath)[1]

    # If cover audio is not in wav format
    if(audioExt != '.wav'):
        # Create a temp folder if it does not exist
        if not os.path.exists("./tmp"):
            os.makedirs("tmp")

        # Convert audio into wav format
        call(["ffmpeg", "-i", audioPath, "tmp/tempaudio.wav", "-y"],stdout=open(os.devnull, "w"), stderr=STDOUT)
        audioPath = os.path.join(os.getcwd(), "tmp/tempaudio.wav")

    #Reading cover audio file
    cover_audio = wave.open(audioPath, mode='rb')
    #Reading audio frames and converting it to byte array
    audio_bytearray = bytearray(list(cover_audio.readframes(cover_audio.getnframes())))

    # Converts the encoded payload string to binary format
    payloadBin = dataToBin(payloadEncode)

    # check if audio_bytearray is big enough for payloadBin
    if len(payloadBin) / LSB_bit > len(audio_bytearray):
        raise ValueError("[!] Insufficient bytes, need bigger cover audio")

    print("Length of cover in Bytes:", len(audio_bytearray))
    print("Length of payload (with delimeter) in Binary:", len(payloadBin)/ LSB_bit)
    
    # Get the length of the encoded payload binary
    payloadLen = len(payloadBin)

    # Setting a local variable to point to the binary value to encode in each iteration
    dataIndex = 0

    print ("[*] Encoding data... \n")
    for i,byte in enumerate(audio_bytearray):
        # If there is still more data to store
        if dataIndex < payloadLen:
            tempBin = ''
            byte = dataToBin(byte)
            # Remove the last few digits of the byte based on the number of LSB used
            byte = byte[:-LSB_bit]
            # Loop and store the data to hide into a temp variable
            for x in range(LSB_bit):
                tempBin += payloadBin[dataIndex]
                dataIndex += 1
                # Break the loop if all the data have been hidden
                if dataIndex == payloadLen:
                    break
            # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
            if len(tempBin) < LSB_bit:
                tempBin = tempBin.ljust(LSB_bit, '0')
            # Adds the temp binary to the byte and change it into an integer and assign it to the back to the array of bytes
            audio_bytearray[i] = int(byte + tempBin, 2)

    # path for output
    path=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop
    name = 'audio_encoded.wav'
    path = ''.join(path)
    output_path = join(path, name)

    # Writing bytes to a new wave audio file, can use mp3 too
    with wave.open(output_path, 'wb') as fd:
        fd.setparams(cover_audio.getparams())
        fd.writeframes(audio_bytearray)

    print("Encoding Successful\n")
    
    # Closes the cover audio
    cover_audio.close()
    

    # Clears the temp folder
    if os.path.exists("./tmp"):
        shutil.rmtree("./tmp")
        
    return(output_path)

def decoding_audio(stego_path,LSB_bit):
    # Opens the embedded audio
    embedded_audio = wave.open(stego_path, mode='rb')
    #Reading frames and converting it to byte array
    audio_bytearray = bytearray(list(embedded_audio.readframes(embedded_audio.getnframes())))

    print ("[*] Decoding data... \n")
    # Extract the LSB based on the value defined by the user
    binaryData = ''
    for i,byte in enumerate(audio_bytearray):
        bin = dataToBin(byte)
        binaryData += bin[-LSB_bit:]
    
    # split the binary data to groups of 8
    allBytes = [binaryData[i: i + 8] for i in range(0, len(binaryData), 8)]

    # converting from bits to characters  
    decodedData = ""  
    for bytes in allBytes:  
        decodedData += chr(int(bytes, 2))  
        # checking if we have reached the delimiter which is "#####"  
        if decodedData[-5:] == "#####":  
            break

    # Removes delimeter
    decodedData = decodedData[:-5]
    # Check if payload is a file or text
    if decodedData[-1:] == '$':
        # Remove '$' from decoded data
        decodedData = decodedData[:-1]
        # Converts the hidden data back to text from a Base64 format
        decodedData = base64.b64decode(eval(decodedData))
        decodedData = decodedData.decode('utf-8')
    else:
        # Get the file extension and removes it
        fileExt = decodedData[-10:]
        decodedData = decodedData[:-10]
        # Remove padding from file extention
        fileExt = fileExt.replace("@", "")
    
        # Converts the hidden data back to a file from a Base64 format
        decodedData = base64.b64decode(eval(decodedData))
        #print(decodedData)

        # path for output
        path=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop
        name = 'decoded_payload'
        path = ''.join(path)
        output_path = join(path, name)
        output_path = output_path+fileExt

        # Write the decoded data back to a file and saves it
        with open(output_path, "wb") as outFile:
            outFile.write(decodedData)
        decodedData = output_path
    print("Decoding Successful\n")
    # Closes the embedded audio
    embedded_audio.close()
    return decodedData

# payload = "payload.txt"
# audio_file = "song_embedded.mp3"
# LSB_bit = int(input("Enter number of LSB to use bitch: "))
# encoding(payload,audio_file,LSB_bit,True)
# print(decoding(LSB_bit))