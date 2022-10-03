import numpy as np
import base64
import os.path
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


# Function to decode the stego and find the payload
def decode_text2(stegoFile, numOfBits):
    print("[*] Decoding data... \n")
    
    # # Get path of stego file
    # stegoPath = os.path.join(os.getcwd(), stegoFile)
    print(stegoFile)
    # Opens the stego file and reads it as bytes
    stegoBytes = ''
    with open(stegoFile, "rb") as stego:
        stegoBytes = stego.read()

    # splitting stegoBytes to binary (8 bits per 1 byte) > xxxxxxxx xxxxxxxx xxxxxxxx
    stegoByteList = []
    stegoBytes = stegoBytes.decode('utf-8')
    for i in range(0, len(stegoBytes)):
        stegoByteList.append(dataToBin(stegoBytes[i]))


    # Extract the LSB based on the value defined by the user
    binaryData = ''
    for i,byte in enumerate(stegoByteList):
        binaryData += byte[-numOfBits:]

    # splitting by 8-bits  (1 byte) [xxxxxxxx,xxxxxxxx, xxxxxxxx]
    allBytes = [binaryData[i: i + 8] for i in range(0, len(binaryData), 8)]

    # converting from bits to characters  
    decodedData = ""  
    for bytes in allBytes:  
        decodedData += chr(int(bytes, 2))  
        # checking if we have reached the delimiter which is "%$&@"  
        if decodedData[-4:] == "%$&@":  
            break
        
    # Removes delimeter
    decodedData = decodedData[:-4]
    # Get the file extension and removes it
    fileExt = decodedData[-10:]
    decodedData = decodedData[:-10]
    # Remove padding from file extention
    fileExt = fileExt.replace("@", "")
    print(decodedData)
    # Converts the hidden data back to a file from a Base64 format
    decodedData = base64.b64decode(eval(decodedData))

    #print(type(decodedData))
    #print(decodedData)
    #decodedStr = decodedData.decode("utf-8") 
    #print(type(decodedStr))
    #print(decodedStr)
    #return decodedStr
    # Write the decoded data back to a file and saves it
    # path for output
    path=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop
    name = 'decoded_output' + fileExt
    path = ''.join(path)
    output_path = join(path, name)
    with open(output_path, "wb") as outFile:
        outFile.write(decodedData)
    return(output_path)

    


# stegoFile = "NANANANA.txt"
# numOfBits = 7
# decode(stegoFile, numOfBits)