# text (cover file) to text (payload) Steganography

import cv2
import numpy as np
import types
import PyPDF2

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

# convert binary to ASCII
def binToStr(bin):
    # Initializing a binary string in the form of
    # 0 and 1, with base of 2
    binInt = int(bin, 2)
    
    # Getting the byte number
    byteNum = binInt.bit_length() + 7 // 8
    
    # Getting an array of bytes
    binArray = binInt.to_bytes(byteNum, "big")
    
    # Converting the array into ASCII text
    ascii_text = binArray.decode()
    
    # Getting the ASCII value
    return ascii_text

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
    #print(len(payloadBin)/ lsb)
    #print(len(coverBin) / 8)
    print ("[*] Encoding data... \n")
    
    '''--Checkpoint--'''
    print("\ncover Binary:" , "(len:", len(coverBin),")" , coverBin, "\n")
    print("payload Binary:","(len:", len(payloadBin), ")", payloadBin , "\n")

    # splitting coverBin to bytes (8 bits per 1 byte) > xxxxxxxx xxxxxxxx xxxxxxxx
    coverBinByte = []
    n  = 8
    for index in range(0, len(coverBin), n):
        coverBinByte.append(coverBin[index : index + n])
 
    # splitting each bit by lsb in payload if lsb = 1 > [x,x,x,x,x,x,x,x] | if lsb = 2 > [xx,xx,xx,xx]
    payloadByLSB = [payloadBin[i:i+lsb] for i in range(0, len(payloadBin), lsb)]
    
    '''--Checkpoint--'''
    #print("Cover by Byte", coverBinByte)
    #print("payload / lsb: ", payloadByLSB)

    # getting the length of bits in payload 
    lenPLBitByLSB = len(payloadByLSB)
    # the counter to check where we at when we are replacing the payload bit inside cover
    bitPL = 0
   
    #print(type(payloadByLSB))

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
    #print("newEncodedBin: ", newEncodedBin)

    # change binary back to ASCII text
    encodedText = binToStr(newEncodedBin)
    print(encodedText)
    return encodedText

def decode (encodedText, lsb):
    print("[*] Decoding data... \n")
    encodedBin = dataToBin(encodedText)
    #print(encodedBin)

    # splitting encodedBin to bytes (8 bits per 1 byte) > xxxxxxxx xxxxxxxx xxxxxxxx
    encodedByte = []
    n = 8
    for index in range(0, len(encodedBin), n):
        encodedByte.append(encodedBin[index : index + n])

    #print(encodedByte)

    # to add the extracted bit out and into here
    payloadBin = ""

    # from each byte take out the last "lsb" (based on whatever the value lsb is)
    for byte in encodedByte:
        #print(byte[-lsb:])
        # add inside the payloadBin
        payloadBin += byte[-lsb:]
    
    '''--Checkpoint--'''
    #print(payloadBin)
    #print(len(payloadBin))
    print("payloadBin: (len:", len(payloadBin), ")", payloadBin)

    while len(payloadBin) % 8 != 0:
        payloadBin += "0"
    
    #print(payloadBin)
    #print(len(payloadBin))
    print("payloadBin: (len:", len(payloadBin), ")", payloadBin)

    # change payloadBin to ASCII - this will be together with the delimeter
    payloadStr = binToStr(payloadBin)
    print("payload + delimeter + random string", payloadStr)
    
    # taking delimeter out of the string
    delimeter = "%$&@"
    payloadTxt = payloadStr.rsplit(delimeter, 1)[0]
    print("payload (secret text): ",payloadTxt)
    return payloadTxt

def openTxtFile(fileName):
    f = open(fileName, "r")
    fileStr = f.read()
    return fileStr


'''--------------------------------------------------------------------------------------------'''

docAsCover = "Hello. My name is Nur Farah Nadiah! I love burger! :)"
secretData = "password is 4321ABC"

cover = "cheeseBurgerme"
payload = "secret"

mate = "cheeseburger"
hide = "hello"


encode(docAsCover, "h", 1)

encodedText = "Hemlo. Lx o`le ir Otr!F`r`i Naeh`i  H lnve burger! :)"
decode(encodedText, 1)