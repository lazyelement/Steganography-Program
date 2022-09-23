#This program is for encoding and decoding audio files
#It works for .wav/mp3 files
#The payload has to be in .txt/.xlsx/.xls/.docx format

from calendar import c
import os
import docx2txt
import pandas as pd
import wave
import numpy as np

def dataToBinary(data):
    if type(data) == str:
        return ''.join([format(ord(i), "08b") for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        return [format(i, "08b") for i in data]
    elif type(data) == int or type(data) == np.uint8:
        return format(data, "08b")
    else:
        # Input type not able to be changed to binary
        raise TypeError("Input type not supported")

def file_type(data):
    #Find extension of file
    split_up = os.path.splitext(data)
    file_extension = split_up[1]
    return file_extension

def convert_to_txt(file_extension,data):
    if '.xlsx' in file_extension:
        xl = pd.ExcelFile(data)

        for sheet in xl.sheet_names:
            file = pd.read_excel(xl,sheet_name=sheet)
            file.to_csv("payload"+'.txt',index=False)
        text_file = open("payload.txt", "r")
        payload = text_file.read()
        text_file.close()
    elif '.docx' in file_extension:
        text = docx2txt.process(data)
        with open("payload.txt", "w") as text_file:
            print(text, file=text_file)
    elif '.txt' in file_extension:
        with open(data, "r") as input:
            # Creating "gfg output file.txt" as output
            # file in write mode
            with open("payload.txt", "w") as output:
                
                # Writing each line from input file to
                # output file using loop
                for line in input:
                    output.write(line)

def encoding(payload,audio_file):
    #Reading cover audio file
    cover_audio = wave.open(audio_file, mode='rb')
    #Reading frames and converting it to byte array
    audio_bytearray = bytearray(list(cover_audio.readframes(cover_audio.getnframes())))

    #Reading the payload
    text_file = open(payload, "r")
    payload = text_file.read()
    text_file.close()

    #Adding extra data ('#') to fill out rest of the bytes
    string = payload + int((len(audio_bytearray)-(len(payload)*8*8))/8) *'#'
    #Converting text to binary list
    binary_list = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))
    n = 0
    # Actual encoding
    # LSB Replacement of the audio data by one bit from audio_bytearray
    for i, bit in enumerate(binary_list):
        if len(binary_list) < n+2:
            break
        else:
            print(n)
            audio_bytearray[i] = (audio_bytearray[i] & 254) | binary_list[n]
            audio_bytearray[i] = (audio_bytearray[i] & 253) | binary_list[n+1]
            n+=2
    #Get the replaced bytes
    frame_replaced = bytes(audio_bytearray)
    # print("hello")

    # embedded_audio = wave.open("song_decoded.wav", mode='rb')

    # audio_list = list(frame_replaced.readframes(frame_replaced.getnframes()))

    # print(audio_list)


    # counter = 0
    # for i in range(len(binary_list)):
    #     if counter < len(binary_list):
    #         temp_bit = []
    #         for x in range(2):
    #             temp_bit.append(binary_list[counter])
    #             counter+=1
    #         audio_bytearray[i] = (audio_bytearray[i] & 254) | temp_bit[0]
    #         audio_bytearray[i] = (audio_bytearray[i] & 253) | temp_bit[1]
    #     else:
    #         break
    # frame_replaced = bytes(audio_bytearray)

    # Write bytes to a new wave audio file
    with wave.open('song_decoded.wav', 'wb') as fd:
        fd.setparams(cover_audio.getparams())
        fd.writeframes(frame_replaced)
    cover_audio.close()

# def decoding():
#     embedded_audio = wave.open("song_decoded.wav", mode='rb')
#     #Reading frames and converting it to byte array
#     audio_bytearray = embedded_audio.readframes(embedded_audio.getnframes())
#     print(type(audio_bytearray))

#     audio_binary=dataToBinary(audio_bytearray)
#     print(type(audio_binary))
#     print(audio_binary)

#     #Extract the LSB of each byte
#     # extracted_LSB = [int((audio_bytearray[i] & 3),2) for i in range(len(audio_bytearray))]
#     # extracted_LSB=""
#     # for i,b in enumerate(audio_binary):
#     #     extracted_LSB+= b[-2:]


#     # print(extracted_LSB)
#     # print(type(extracted_LSB))


#     # # string=''
#     # # for x in extracted_LSB:
#     # #     string += ''+str(x)
#     # # print(string)
#     # # if '3'in string:
#     # #     print("djiksakd")
#     # #Convert byte array back to string
#     # # embedded_text = "".join(chr(int("".join(map(str,extracted_LSB[i:i+8])),2)) for i in range(0,len(extracted_LSB),8))
#     # embedded_text = [string[i: i+8] for i in range(0, len(string), 8)]
#     # print()
#     # #Cut off at the filler characters
#     # # decoded_text = embedded_text.split("###")[0]
#     # decodedData = ""
#     # for byte in embedded_text:
#     #     decodedData += chr(int(byte, 2))
#     #     if "###" in decodedData: # Stop decoding after we have reached the delimeter which is "#####"
#     #         break
#     # ascii_string = ""
#     # for binary_value in extracted_LSB:
#     #     an_integer = int(binary_value, 2)



#     #     ascii_character = chr(an_integer)



#     #     ascii_string += ascii_character

#     # Print the extracted text
#     print("Payload is: "+ascii_string)
#     embedded_audio.close()

def decoding():
    embedded_audio = wave.open("song_decoded.wav", mode='rb')
    #Reading frames and converting it to byte array
    audio_bytearray = list(embedded_audio.readframes(embedded_audio.getnframes()))

    print(audio_bytearray)

    #Extract the LSB of each byte
    extracted_LSB = [audio_bytearray[i] & 1 for i in range(len(audio_bytearray))]
    print(extracted_LSB)
    #Convert byte array back to string
    embedded_text = "".join(chr(int("".join(map(str,extracted_LSB[i:i+8])),2)) for i in range(0,len(extracted_LSB),8))
    print(embedded_text)
    #Cut off at the filler characters
    decoded_text = embedded_text.split("###")[0]

    # Print the extracted text
    print("Payload is: "+decoded_text)
    embedded_audio.close()

data = "cover.txt"
convert_to_txt(file_type(data),data)
payload = "payload.txt"
audio_file = "song_embedded.mp3"
encoding(payload,audio_file)
decoding()

