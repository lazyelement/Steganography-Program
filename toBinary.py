def decimalToBinary(n):
    return bin(n).replace("0b", "")

def fileToBinary(file):
    
    with open(file,'rb') as f:
        file_content = f.read()

    f.close()

    output = list(file_content)
    newlist = []
    for i in output:
        newlist.append(decimalToBinary(int(i)))

    outputBinary = ''
    for i in newlist:
        outputBinary += i

    print(file_content)
    return outputBinary

def byteCounter(string):
    return len(string)/8

print(fileToBinary("cover.txt"))
print(fileToBinary("payload.txt"))
print(fileToBinary("imageFile.jpeg"))



