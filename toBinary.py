import cv2
import numpy as np
from PIL import Image
import os
import time

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
# cover file is fixed at image
def encode(img_name, payload, choice, lsb):
    #choice:
    #1: indicates that payload is a text file
    #2: indicates payload is img file
    #3: indicates payload is audio file
    #4: indiciates payload is video file
    if img_name[-3:]=="jpg" or img_name[-4:] == "jpeg":
        newimg = Image.open(img_name)
        newimg.save("temp.png")
        cover_img = cv2.imread("temp.png")
        os.remove("temp.png")
    
    else:
        cover_img = cv2.imread(img_name)

    # calculating the maximum bytes for encoding
    nBytes = cover_img.shape[0] * cover_img.shape[1] * 3 // 8

    if choice == 1:
        f = open(payload,"r")
        secret_msg = f.read()

        print("Maximum Bytes for encoding:", nBytes)
        secret_msg += '#####'       # we can utilize any string as the delimiter

        # checking whether the number of bytes for encoding is less  
        # than the maximum bytes in the image  
        if len(secret_msg) > nBytes:  
            raise ValueError("Error encountered insufficient bytes, need bigger image or less data!!")  
        
        dataIndex = 0  
        # converting the input data to binary format using the msg_to_bin() function  
        bin_secret_msg = msg_to_bin(secret_msg)
        
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
                    pixels[0] = int(r[:-1] + bin_secret_msg[dataIndex], 2)  
                    dataIndex += 1  
                if dataIndex < dataLen:  
                    # hiding the data into LSB of Green pixel  
                    pixels[1] = int(g[:-1] + bin_secret_msg[dataIndex], 2)  
                    dataIndex += 1  
                if dataIndex < dataLen:  
                    # hiding the data into LSB of Blue pixel  
                    pixels[2] = int(b[:-1] + bin_secret_msg[dataIndex], 2)  
                    dataIndex += 1  
                # if data is encoded, break out the loop  
                if dataIndex >= dataLen:  
                    break  
        stego_file_name = "stego_"+img_name
        if stego_file_name[-3:]=="jpg":
            stego_file_name = stego_file_name[0:-3]+"png"
        elif stego_file_name[-4:] == "jpeg":
            stego_file_name = stego_file_name[0:-4]+"png"
        cv2.imwrite(stego_file_name,cover_img)
        return 1
    
    elif choice == 2:
        # need to find a way to add delimitter to np array
        secret_img = cv2.imread(payload)
        sBytes = secret_img.size
        #print(secret_img)
        np.append(secret_img,([[1,2,3]]*secret_img.shape[0]))
        print(secret_img)

    elif choice == 3:
        pass

    elif choice == 4:
        pass

def decode(img_name):  

    img = cv2.imread(img_name)

    
    bin_data = ""  
    
    for values in img:  
        for pixels in values:  
            # converting the Red, Green, Blue values into binary format  
            r, g, b = msg_to_bin(pixels)  
            # data extraction from the LSB of Red pixel  
            bin_data += r[-1]  
            # data extraction from the LSB of Green pixel  
            bin_data += g[-1]  
            # data extraction from the LSB of Blue pixel  
            bin_data += b[-1]  

    # splitting by 8-bits  
    allBytes = [bin_data[i: i + 8] for i in range(0, len(bin_data), 8)]  
    # converting from bits to characters  
    decodedData = ""  
    for bytes in allBytes:  
        decodedData += chr(int(bytes, 2))  
        # checking if we have reached the delimiter which is "#####"  
        if decodedData[-5:] == "#####":  
            break   
    # removing the delimiter to display the actual hidden message  
    return decodedData[:-5]  



encode("sample.png","payload.txt",1,0)

time.sleep(3)

print(decode("stego_sample.png"))




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


