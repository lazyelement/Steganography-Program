import os
import cv2
import base64
import numpy as np

# converting types to binary  
def msg_to_bin(msg):
    if type(msg) == str:
        return ''.join([format(ord(i), "08b") for i in msg])
    elif type(msg) == bytes or type(msg) == np.ndarray:
        return [format(i, "08b") for i in msg]
    elif type(msg) == int or type(msg) == np.uint8:  
        return format(msg, "08b")  
    else:
        raise TypeError("Input type not supported")

def encode_img(coverFile, payloadFile, lsb):   

    if lsb<1 or lsb>8:
        print("Incorrect input please try from 1-8")
        return False
    #Reads in the cover image data  
    cover_img = cv2.imread(coverFile)

    # Opens the payload object and encodes it into a Base64 format
    payloadB64 = ''
    with open(payloadFile, "rb") as payload:
        payloadB64 = base64.b64encode(payload.read())
    

    # Gets the extension of the payload
    payloadExt = os.path.splitext(payloadFile)[1]

    #Pad the extension to get length of 5 to identify the file extension during decoding
    while len(payloadExt)<5:
        payloadExt+="@"

    # Combine and generate the secret message to encode into cover
    payloadEncode = str(payloadB64)+payloadExt+"#####"
    secret_msg = msg_to_bin(payloadEncode)
    
    #check number of channels for the image (3 is RGB and 4 is RGBA)
    channels = cover_img.shape[2]

    # calculating the maximum bytes for encoding
    nBytes = cover_img.shape[0] * cover_img.shape[1] * 3 // 8
    sBytes = len(secret_msg)

    # Checks if the cover file is big enough to hide the payload
    if sBytes > nBytes:
        raise ValueError("Error encountered insufficient bytes, need bigger image or less data!!")
    
    # Adds empty bits to the end of message to make into perfect byte size
    while len(secret_msg)%lsb!=0:
        secret_msg += "0"
    
    dataLen = len(secret_msg)

    dataIndex = 0

    # Iterate through the columns and rows of pixels of the cover image to encode the payload data into
    for values in cover_img:
        for pixel in values:
            if channels == 3:
                r, g, b = msg_to_bin(pixel)
            elif channels == 4:
                r, g, b, a = msg_to_bin(pixel)
            
            # hides appropriate lsb worth of data into the red pixel
            if dataIndex<dataLen:
                pixel[0] = int(r[:-lsb] + secret_msg[dataIndex:dataIndex+lsb],2)
                dataIndex += lsb

            # hides appropriate lsb worth of data into the green pixel
            if dataIndex<dataLen:
                pixel[1] = int(g[:-lsb] + secret_msg[dataIndex:dataIndex+lsb],2)
                dataIndex += lsb
            
            # hides appropriate lsb worth of data into the blue pixel
            if dataIndex<dataLen:
                pixel[2] = int(b[:-lsb] + secret_msg[dataIndex:dataIndex+lsb],2)
                dataIndex += lsb

            # hides appropriate lsb worth of data into the alpha pixel if the image is in RGBA format
            if dataIndex<dataLen and channels == 4:
                pixel[3] = int(a[:-lsb] + secret_msg[dataIndex:dataIndex+lsb],2)
                dataIndex += lsb
            
            # If the number of bits to hide has all been hidden, break the loop
            if dataIndex >= dataLen:
                break
    
    # Format the name of the file to save the encoded image as
    coverName = os.path.splitext(coverFile)[0]
    coverName = coverName+"_encoded"
    saveAs = coverName+".png"

    # Write out the encoded image 
    cv2.imwrite(saveAs, cover_img)
    print("Saved encoded file as ", saveAs)
    return saveAs


def decode_img(imgFile, lsb):
    if lsb<1 or lsb>8:
        print("Incorrect input please try from 1-8")
        return False
    # Read in the stego image data
    img = cv2.imread(imgFile)

    # Get what type of format the image is in whether RGB or RGBA
    channels = img.shape[2]

    # Initialise string to contain the binary data from the encoded file
    bin_data = ""

    # Iterate through the columns and rows of pixel data in the image to extract the bit data out
    for values in img:
        for pixel in values:
            if channels == 3:
                r, g, b = msg_to_bin(pixel)
                bin_data += r[-lsb:]
                bin_data += g[-lsb:]
                bin_data += b[-lsb:]
            elif channels == 4:
                r, g, b, a = msg_to_bin(pixel)
                bin_data += r[-lsb:]
                bin_data += g[-lsb:]
                bin_data += b[-lsb:]
                bin_data += a[-lsb:]
    
    # Store the binary data as bytes per entry in allByte list
    allBytes = [bin_data[i:i+8] for i in range(0,len(bin_data),8)]

    # Iterate through the byte list and convert each byte back into ascii 
    decodedData = ""
    for byte in allBytes:
        decodedData += chr(int(byte,2))
        if decodedData[-5:] == "#####":
            break

    # Remove the delimitter
    decodedData = decodedData[:-5]

    # Get the file extentsion of the original payload to save it as
    fileExt = decodedData[-5:]
    fileExt = fileExt.replace("@", "")

    # Get the actual data of the payload by removing the extension
    decodedData = decodedData[:-5]

    # Get the name to format the name of decoded file as
    imgFile = os.path.splitext(imgFile)[0]
    
    # Decode base64 formatted decoded data back into byte data to save the file as
    decodedData = base64.b64decode(eval(decodedData))
    imgFile = imgFile.replace("encoded","decoded")
    saveAs = imgFile + fileExt
    with open(saveAs, "wb") as outFile:
        outFile.write(decodedData)

    print("Saved decoded file as ", saveAs)

    return saveAs


# encode("sample.png","payload",1)

#decode("encoded_sample.png",1)
