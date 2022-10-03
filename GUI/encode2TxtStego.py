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


# Function to hide payload inside cover
def encode_text2(coverFile, payloadFile, numOfBits):
    # Get path of cover file and payload file
    coverPath = os.path.join(os.getcwd(), coverFile)
    payloadPath = os.path.join(os.getcwd(), payloadFile)

    # Opens the cover file and reads it as bytes
    coverBytes = ''
    with open(coverPath, "rb") as cover:
        coverBytes = cover.read()


    # Opens the payload file and encodes it into a Base64 format
    payloadB64 = ''
    with open(payloadPath, "rb") as payload:
        payloadB64 = base64.b64encode(payload.read())

    # Find extension of payload file
    coverExt = os.path.splitext(coverPath)[1]
    payloadExt = os.path.splitext(payloadPath)[1]

    # Add padding to file extention untill there is 10 characters
    while len(payloadExt) < 10:
        payloadExt += '@'

    # Converts the encoded Base64 payload into a string and adds the file extention and the delimeter to indicate the end of the file
    payloadEncode = str(payloadB64) + payloadExt + "%$&@"

    # Converts the encoded payload string to binary format
    payloadBin = dataToBin(payloadEncode)

    print("Length of cover in Bytes:", len(coverBytes))
    print("Length of payload (with delimeter) in Binary:", len(payloadBin)/ numOfBits)

    # check if coverBytes is big enough for payloadBin
    if len(payloadBin) / numOfBits > len(coverBytes):
        raise ValueError("[!] Insufficient bytes, need bigger cover document")
    
    print ("[*] Encoding data... \n")
    
    '''--Checkpoint--''' # Can put to comment 
    #print("\ncover Base 64:" , "(len:", len(coverB64),")" , coverB64, "\n")
    #print("payload Binary:","(len:", len(payloadBin), ")", payloadBin , "\n")

    # splitting coverBytes to binary (8 bits per 1 byte) > xxxxxxxx xxxxxxxx xxxxxxxx
    coverByteList = []
    coverBytes = coverBytes.decode('utf-8')
    for i in range(0, len(coverBytes)):
        coverByteList.append(dataToBin(coverBytes[i]))
    
    # Get the length of the encoded payload binary
    payloadLen = len(payloadBin)

    # Setting a local variable to point to the binary value to encode in each iteration
    dataIndex = 0

    for i,byte in enumerate(coverByteList):
        # If there is still more data to store
        if dataIndex < payloadLen:
            tempBin = ''
            # Remove the last few digits of the byte based on the number of LSB used
            byte = byte[:-numOfBits]
            # Loop and store the data to hide into a temp variable
            for x in range(numOfBits):
                tempBin += payloadBin[dataIndex]
                dataIndex += 1
                # Break the loop if all the data have been hidden
                if dataIndex == payloadLen:
                    break
            # Pad 0 to the front of the temp binary if the length of the temp binary is less than the number of LSB used
            if len(tempBin) < numOfBits:
                tempBin = tempBin.ljust(numOfBits, '0')
            # Adds the temp binary to the byte and change it into an integer and assign it to the back to the array of bytes
            coverByteList[i] = byte + tempBin

    # converting from bits to characters  
    encodedText = ""  
    for bytes in coverByteList:  
        encodedText += chr(int(bytes, 2))
    
    print("\nEncoded Text(Stego):", encodedText)
    print("Encoded Text Length:", len(encodedText), "\n")
    print("########### Encoding Successful ###########\n")
    
    # path for output
    path=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop
    name = 'encoded_output' + coverExt
    path = ''.join(path)
    output_path = join(path, name)
    # Saves ouput into a file
    with open(output_path, "wb") as outFile:
            outFile.write(encodedText.encode('utf-8'))
    
    return(output_path)



# coverFile = "cover.txt"
# #coverFile = "egDoc.docx"
# payloadFile = "payload.JPG"
# numOfBits = 7
# encode(coverFile, payloadFile, numOfBits)