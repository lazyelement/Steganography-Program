

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


encodeSideBinary = fileToBinary("imageFile.jpeg")

#to create new image file
binaryToFile(encodeSideBinary, "outputFile.jpeg")