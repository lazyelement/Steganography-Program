
import cv2
import numpy as np
from PIL import Image
import os
import os.path
import base64


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


# defining function to hide the secret message into the image  
# coverFile: cover image's file name with extension can be jpeg, png, bmp
# payloadFile: payload's file name with extension can be jpg, png, bmp
# saveAs: file name of output encoded with extension for image can only be in png
def encode(coverFile, payloadFile, saveAs, choice, lsb):
    #choice:
    #1: indicates that payload is a text file
    #2: indicates payload is img file
    #3: indicates payload is audio file
    #4: indiciates payload is video file
    if lsb<1 or lsb>7:
        return "Invalid number of LSB. Please enter a number from 1-7"

    if choice == 1:
        if coverFile[-3:]=="jpg" or coverFile[-4:] == "jpeg":

            #Convert cover image to png format
            newimg = Image.open(coverFile)
            newimg.save("temp.png")
            cover_img = cv2.imread("temp.png")
            os.remove("temp.png")
        
        else:
            cover_img = cv2.imread(coverFile)

        # calculating the maximum bytes for encoding
        nBytes = cover_img.shape[0] * cover_img.shape[1] * 3 // 8

        f = open(payloadFile,"r")
        payload_msg = f.read()

        print("Maximum Bytes for encoding:", nBytes)
        payload_msg += '#####'       # we can utilize any string as the delimiter

        # checking whether the number of bytes for encoding is less  
        # than the maximum bytes in the image  
        if len(payload_msg) > nBytes:  
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data!!")  
        
        dataIndex = 0  
        # converting the input data to binary format using the msg_to_bin() function  
        bin_secret_msg = msg_to_bin(payload_msg)
        print(bin_secret_msg)
        # finding the length of data that requires to be hidden  
        dataLen = len(bin_secret_msg)  

        for values in cover_img:  
            for pixels in values:  
                # convert RGB values to binary format
                r, g, b = msg_to_bin(pixels)
                # modifying the LSB only if there is data remaining to store  
                if dataIndex < dataLen:  
                    # hiding the data into LSB of Red pixel  
                    #r[:-1] -> gets the binary data up till, not including, the lsb, so the first 7 bits
                    #then it adds the payload's according bit to the end and wrap it up as a new decimal value
                    #int wrap converts the binary to decimal form
                    pixels[0] = int(r[:-lsb] + bin_secret_msg[dataIndex:dataIndex+lsb], 2)  
                    dataIndex += lsb  
                if dataIndex< dataLen:  
                    # hiding the data into LSB of Green pixel  
                    pixels[1] = int(g[:-lsb] + bin_secret_msg[dataIndex:dataIndex+lsb], 2)  
                    dataIndex += lsb  
                if dataIndex< dataLen:  
                    # hiding the data into LSB of Blue pixel  
                    pixels[2] = int(b[:-lsb] + bin_secret_msg[dataIndex:dataIndex+lsb], 2)  
                    dataIndex += lsb  
                # if data is encoded, break out the loop  
                if dataIndex>= dataLen:  
                    break  

        cv2.imwrite(saveAs, cover_img)
        return 1
    
    elif choice == 2:
        # need to find a way to add delimitter to np array

        payload_img = cv2.imread(payloadFile)
        cover_img = cv2.imread(coverFile)

        # calculating the maximum bytes for encoding
        nBytes = cover_img.shape[0] * cover_img.shape[1] * 3 // 8
        sBytes = payload_img.size

        # Encode the payload image into a Base64 format
        payloadExt = os.path.splitext(payloadFile)[1]
        _, payloadArr = cv2.imencode(payloadExt,payload_img)
        payloadB64 = base64.b64encode(payloadArr.tobytes())

        if sBytes > nBytes:
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data!!")
        
        #check number of channels for the image (3 is RGB and 4 is RGBA)
        channels = cover_img.shape[2]

        payloadEncode = str(payloadB64)+"#####"
        secret_msg = msg_to_bin(payloadEncode)

        while len(secret_msg)%lsb!=0:
            secret_msg += "0"
        
        dataLen = len(secret_msg)

        dataIndex = 0

        for values in cover_img:
            for pixel in values:
                if channels == 3:
                    r, g, b = msg_to_bin(pixel)
                elif channels == 4:
                    r, g, b, a = msg_to_bin(pixel)
                
                if dataIndex<dataLen:
                    pixel[0] = int(r[:-lsb] + secret_msg[dataIndex:dataIndex+lsb],2)
                    dataIndex += lsb

                if dataIndex<dataLen:
                    pixel[1] = int(g[:-lsb] + secret_msg[dataIndex:dataIndex+lsb],2)
                    dataIndex += lsb
                
                if dataIndex<dataLen:
                    pixel[2] = int(b[:-lsb] + secret_msg[dataIndex:dataIndex+lsb],2)
                    dataIndex += lsb

                if dataIndex<dataLen and channels == 4:
                    pixel[3] = int(a[:-lsb] + secret_msg[dataIndex:dataIndex+lsb],2)
                    dataIndex += lsb
                
                if dataIndex >= dataLen:
                    break
        
        cv2.imwrite(saveAs, cover_img)
        return 1

    elif choice == 3:
        pass

    elif choice == 4:
        pass

    else:
        return "Invalid choice option. Please enter valid choice number."

#img_name: file name with extension of stego file
#saveAs: file name with extension of payload to be written into
def decode(img_name, saveAs, choice, lsb):  
    #choice:
    #1: indicates that payload is a text file
    #2: indicates payload is img file
    #3: indicates payload is audio file
    #4: indiciates payload is video file

    img = cv2.imread(img_name)

    
    bin_data = ""  
    
    if choice == 1:
        for values in img:  
            for pixels in values:  
                # converting the Red, Green, Blue values into binary format  
                r, g, b = msg_to_bin(pixels)  
                # data extraction from the LSB of Red pixel  
                bin_data += r[-lsb:]  
                #print(bin_data)
                # data extraction from the LSB of Green pixel  
                bin_data += g[-lsb:]  
                # data extraction from the LSB of Blue pixel  
                bin_data += b[-lsb:]  

        # splitting by 8-bits  
        allBytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]  
        # converting from bits to characters  
        decodedData = ""  
        for bytes in allBytes:  
            decodedData += chr(int(bytes, 2))  
            # checking if we have reached the delimiter which is "#####"  
            if decodedData[-5:] == "#####":  
                break
        

        #print(decodedData)
        with open(saveAs,"w") as f:
            f.write(decodedData[:-5])
            f.close()
        
    
    if choice == 2:
        channels = img.shape[2]

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
        #print(bin_data)
        allBytes = [bin_data[i:i+8] for i in range(0,len(bin_data),8)]

        decodedData = ""
        for byte in allBytes:
            decodedData += chr(int(byte,2))
            if decodedData[-5:] == "#####":
                break
        
        #print(decodedData)
        decodedData = eval(decodedData[:-5])
        decodedArr = np.frombuffer(base64.b64decode(decodedData),dtype=np.uint8)
        decodedImg = cv2.imdecode(decodedArr,flags=cv2.IMREAD_COLOR)

        cv2.imwrite(saveAs,decodedImg)
        
    

encode("catTest.bmp","payload.jpg","stego_output.png",2,5)

# decode("stego_output.png","output_payload.png",2,5)


# defining function to encode data into Image  
# def encodeText():  
#     img_name = input("Enter image name (with extension): ")  
    
#     # reading the input image using OpenCV-Python  
#     if img_name[-3] == "jpg" or img_name[-4] == "jpeg":

#         newimg = Image.open(img_name)
#         newimg.save("temp.png")
#         img = cv2.imread("temp.png")
    
#     else:
#         img = cv2.imread(img_name)
#     # printing the details of the image  
#     print("The shape of the image is: ", img.shape) # checking the image shape to calculate the number of bytes in it  
#     print("The original image is as shown below: ")  

#     data = input("Enter data to be encoded: ")  
#     if (len(data) == 0):  
#         raise ValueError('Data is Empty')  
      
#     file_name = input("Enter the name of the new encoded image (with extension): ")  
#     # calling the hide_data() function to hide the secret message into the selected image
    
#     #put in function to replace the extension jpeg or jpg with png 
#     #just totally remove 

#     encodedImage = hide_data(img, data)

#     #delete the png file after it outputs the jpeg file

#     cv2.imwrite(file_name, encodedImage)


# # defining the function to decode the data in the image  
# def decodeText():  
#     # reading the image containing the hidden image  
#     img_name = input("Enter the name of the Steganographic image that has to be decoded (with extension): ")  
    
#     img = cv2.imread(img_name)  # reading the image using the imread() function  
#     #Problem over here the image that is reading supppose to have stego rgb values but is showing cover rgb values
#     print("The Steganographic image is as follow: ")
#     text = show_data(img)  
#     return text

# image steganography  
# def steganography():  
#     n = int(input("Image Steganography \n1. Encode the data \n2. Decode the data \n Select the option: "))  
#     if (n == 1):  
#         print("\nEncoding...")  
#         encodeText()  
  
#     elif (n == 2):  
#         print("\nDecoding...")  
#         print("Decoded message is " + decodeText())  
      
#     else:  
#         raise Exception("Inserted value is incorrect!")  
  
# steganography() # encoding the image  

'''
def fileToBinary(file):
    
    #open the file and read it as byte data
    with open(file,'rb') as f:
        file_content = f.read()
    f.close()

    #convert byte data into hex format
    hexaVal=file_content.hex()

    #convert hex format to binary ---> int(hexaVal,16) turns the hex to decimal then binturns decimal to binary
    result = bin(int(hexaVal,16))

    #strip the 0b at the start to turn it to pure binary
    stripped_result = result[2:]
    return stripped_result

def binaryToFile(stripped_binary, filename):
    #reverse order
    #first convert binary to hex
    binary = "0b"+stripped_binary
    hexaVal = hex(int(binary,2))[2:]

    file_content = bytes.fromhex(hexaVal)

    #to write the byte data into a file

    f = open(filename,"wb")
    f.write(file_content)
    f.close()

    #print(hexaVal)


def byteCounter(string):
    return len(string)/8

def splitter(binary):
    split_bin = wrap(binary,8)
    string_bin = ' '.join(map(str,split_bin))
    return string_bin
# encodeSideBinary = fileToBinary("imageFile.jpeg")

# #to create new image file
# binaryToFile(encodeSideBinary, "outputFile.jpeg")

''''''Following is still under construction''''''

cover = fileToBinary("imageFile.jpeg")
payload = fileToBinary('payload.txt')
# print(splitter(payload))
# print("this is cover: ",splitter(cover))
def lsb_replacement(cover,payload):
    list_cover = list(cover)
    list_payload = list(payload)

    #this is only for if LSB setting is 1 bit

    counter = 31
    pointer = 0
    #the following is only assuming that the cover file is big enough for payload
    while pointer< len(list_payload):
        list_cover[counter] = list_payload[pointer]
        counter += 8
        pointer += 1
    
    output = "".join(list_cover)

    return output

stego_binary = lsb_replacement(cover,payload)
# print("this is stego: ",splitter(stego_binary))
binaryToFile(stego_binary,"newFile.jpeg")'''


