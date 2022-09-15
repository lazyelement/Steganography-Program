def decimalToBinary(n):
    return bin(n).replace("0b", "")

with open('imageFile.jpeg','rb') as f:
    file_content = f.read()

f.close()

output = list(file_content)
newlist = []
for i in output:
    newlist.append(decimalToBinary(int(i)))

outputBinary = ''
for i in newlist:
    outputBinary += i

print(outputBinary)

#Translated the file into binary data (string format)












