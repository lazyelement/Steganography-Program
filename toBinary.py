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












