# text (cover file) to text (payload) Steganography
# currently can only do 1 lsb

import numpy as np

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
def encode(cover, payload, lsb):
    # Add delimeter to secret data
    payload += "%$&@"

    # change data to Binary
    coverBin = dataToBin(cover)
    payloadBin = dataToBin(payload)

    #print(len(payloadBin))
    #print(len(coverBin))

    # check if coverData is big enough for payloadData
    if len(payloadBin) / lsb > len(coverBin) / 8:
        raise ValueError("[!] Insufficient bytes, need bigger cover document")
    
    print("Length of cover (by Bytes) in Binary:", len(coverBin) / 8)
    print("Length of payload (with delimeter) in Binary:", len(payloadBin)/ lsb)
    print ("[*] Encoding data... \n")
    
    '''--Checkpoint--''' # Can put to comment 
    print("\ncover Binary:" , "(len:", len(coverBin),")" , coverBin, "\n")
    print("payload Binary:","(len:", len(payloadBin), ")", payloadBin , "\n")

    # splitting coverBin to bytes (8 bits per 1 byte) > xxxxxxxx xxxxxxxx xxxxxxxx
    coverBinByte = []
    n  = 8
    for index in range(0, len(coverBin), n):
        coverBinByte.append(coverBin[index : index + n])
 
    # splitting each bit by lsb in payload if lsb = 1 > [x,x,x,x,x,x,x,x] | if lsb = 2 > [xx,xx,xx,xx]
    payloadByLSB = [payloadBin[i:i+lsb] for i in range(0, len(payloadBin), lsb)]
    
    '''--Checkpoint--''' # Can put to comment
    #print("Cover by Byte", coverBinByte)
    #print("payload / lsb: ", payloadByLSB)

    # getting the length of bits in payload 
    lenPLBitByLSB = len(payloadByLSB)
    # the counter to check where we at when we are replacing the payload bit inside cover
    bitPL = 0
   
    #print("payloadByLSB type: ", type(payloadByLSB))

    coverBinBit = list(coverBin)
    #print(coverBinBit)
    
    '''--------LIMITATIONS--------'''
    # this code works only for 1 lsb. i have not try for more than 1 lsb
    for i in range(7, len(coverBinBit), 8):
        if bitPL < len(payloadBin):
            coverBinBit [i] = payloadBin[bitPL]
            bitPL += 1
        if bitPL >= len(payloadBin):
            break

    # join all the bit together
    newEncodedBin = "".join(coverBinBit)
    print("newEncodedBin: ", newEncodedBin)

    # splitting by 8-bits  
    allBytes = [newEncodedBin[i: i + 8] for i in range(0, len(newEncodedBin), 8)]  
    # converting from bits to characters  
    encodedText = ""  
    for bytes in allBytes:  
        encodedText += chr(int(bytes, 2))  
    
    print("\nEncoded Text(Stego):", encodedText, "\n")
    print("########### Encoding Successful ###########\n")
    return encodedText


# Function to decode the stego and find the payload
def decode (encodedText, lsb):
    print("encoded text: (len:", len(encodedText), ")" ,encodedText, "\n")
    print("[*] Decoding data... \n")
    
    encodedBin = dataToBin(encodedText)
    print("Stego data in binary: ", encodedBin, "\n")

    
    # splitting encodedBin to bytes (8 bits per 1 byte) > xxxxxxxx xxxxxxxx xxxxxxxx
    encodedByte = []
    n = 8
    for index in range(0, len(encodedBin), n):
        encodedByte.append(encodedBin[index : index + n])
    #print("Binary stego in bytes: ", encodedByte, "\n")

    # to add the extracted bit out and into here
    payloadBin = ""
    
    # from each byte take out the last "lsb" (based on whatever the value lsb is)
    for byte in encodedByte:
        #print(byte[-lsb:])
        # add inside the payloadBin
        payloadBin += byte[-lsb:]
    
    '''--Checkpoint--'''
    print("payloadBin: (len:", len(payloadBin), ")", payloadBin, "\n")

    # delimeter
    delimeter = "%$&@"

    # splitting by 8-bits  (1 byte) [xxxxxxxx,xxxxxxxx, xxxxxxxx]
    allBytes = [payloadBin[i: i + 8] for i in range(0, len(payloadBin), 8)]
    
    #print(allBytes, "\n")
    
    # converting from bits to characters  
    decodedData = ""  
    for bytes in allBytes:  
        decodedData += chr(int(bytes, 2))  
        # checking if we have reached the delimiter which is "%$&@"  
        if decodedData[-4:] == delimeter:  
            break
    
    print("Secret data with delimeter:", decodedData)
    
    payloadTxt = decodedData.rsplit(delimeter, 1)[0]
    print("Payload (secret text):",payloadTxt, "\n")
    return payloadTxt


# Function to open .txt file
def openTxtFile(fileName):
    f = open(fileName, "r")
    fileStr = f.read()
    return fileStr

# Function to save string to .txt file !!FILENAME NEED TO HAVE .TXT!!
def saveTxtToFile (string, fileName):
    text_file = open(fileName, "w")
    #write string to file
    text_file.write(string)
    #close file
    text_file.close()


'''--------------------------------------------------------------------------------------------'''

cover = "HELLO THERE THIS IS A TEST TEXT FILE I dont know what else to type in here to make this file bigger so here i am rambling and typing nonsense"
payload = "No"

stego = encode(cover, payload, 1)
secretData = decode(stego,1)


#decode(encode(cover, payload, 1), 1)

# Save to txt file
#saveTxtToFile(secretData, "secretData.txt")