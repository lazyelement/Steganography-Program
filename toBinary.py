from textwrap import wrap

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


def byteCounter(string):
    return len(string)/8

def splitter(binary):
    split_bin = wrap(binary,8)
    string_bin = ' '.join(map(str,split_bin))
    return string_bin
# encodeSideBinary = fileToBinary("imageFile.jpeg")

# #to create new image file
# binaryToFile(encodeSideBinary, "outputFile.jpeg")

'''Following is still under construction'''

cover = fileToBinary("imageFile.jpeg")
payload = fileToBinary('catTest.jpeg')
# print(splitter(payload))
# print("this is cover: ",splitter(cover))
def lsb_replacement(cover,payload):
    list_cover = list(cover)
    list_payload = list(payload)

    #this is only for if LSB setting is 1 bit

    counter = 7
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
binaryToFile(stego_binary,"newFile.jpeg")




