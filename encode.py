# 1) Convert data to binary - Done
# 2) Identify file format - Done
# 3) Split string into 8 chars - Done
# 4) AND operation -  Not Done
# 5) Bro damn confusing sia idk how do this algo

import cv2, numpy as np, os
from textwrap import wrap

data = "30secvid.mp4"

#Find extension of file
split_tup = os.path.splitext(data)
file_extension = split_tup[1]
print("File Extension: ", file_extension)

#Get binary value of file
if isinstance(data,str):
    binary = ''.join([format(ord(i),"08b") for i in data])
    print(binary)
elif isinstance(data, bytes) or isinstance(data,np.ndarray):
    binary = [format(i,"08b") for i in data]
elif isinstance(data, int) or isinstance(data,np.uint8):
    binary = format(data,"08b")
else:
    print(TypeError("Type not supported"))

#Split string into 8 chars
split_bin = wrap(binary,8)
string_bin = ' '.join(map(str,split_bin))
print(string_bin)

#and operation in python
string = '1111'
string_bin = '0b' + string

int(string_bin)

#print(int(string_bin))

base = '1100'
base_bin = '0b' + base

# print("a&b: ",bin(int(string_bin)&int(base_bin)))
#print(bin(string) & bin(base))

