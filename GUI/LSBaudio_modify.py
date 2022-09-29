#This program is for encoding and decoding audio files
#It works for .wav/mp3 files
#The payload has to be in .txt/.xlsx/.xls/.docx format

import os
import docx2txt
import pandas as pd #pip install pandas
import wave
from pathlib import Path
from os.path import join

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./output") 

#get file extension
def file_type(data):
    #Find extension of file
    split_up = os.path.splitext(data)
    file_extension = split_up[1]
    return file_extension

#to change file type to txt
def convert_to_txt(file_extension,data):
    #if format is excel
    if '.xlsx' in file_extension:
        xl = pd.ExcelFile(data)

        for sheet in xl.sheet_names:
            file = pd.read_excel(xl,sheet_name=sheet)
            file.to_csv("payload"+'.txt',index=False)
        text_file = open("payload.txt", "r")
        payload = text_file.read()
        text_file.close()
    elif '.xls' in file_extension:
        xl = pd.ExcelFile(data)

        for sheet in xl.sheet_names:
            file = pd.read_excel(xl,sheet_name=sheet)
            file.to_csv("payload"+'.txt',index=False)
        text_file = open("payload.txt", "r")
        payload = text_file.read()
        text_file.close()
    #if format is .docx
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

def encoding_audio(payload,audio_file,LSB_bit):
    #Reading cover audio file
    cover_audio = wave.open(audio_file, mode='rb')
    #Reading frames and converting it to byte array
    audio_bytearray = bytearray(list(cover_audio.readframes(cover_audio.getnframes())))

    #Reading the payload
    if(payload.endswith(".txt")):
        text_file = open(payload, "r")
        payload = text_file.read()
        text_file.close()
    else:
        payload = payload

    #Adding extra data ('#') to fill out rest of the bytes
    string = payload + int((len(audio_bytearray)-(len(payload)*8*8))/8) *'#'
    #Converting text to binary list
    binary_list = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in string])))

    # Actual encoding
    # LSB Replacement of the audio data by one bit from audio_bytearray
    if LSB_bit == 0:
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 254) | bit
    elif LSB_bit == 1:
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 253) | binary_list[bit+1] #to take 2nd number in binary list
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 254) | bit
    elif LSB_bit == 2:
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 251) | binary_list[bit+2]#to take 3rd number in binary list
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 253) | binary_list[bit+1]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 254) | bit
    elif LSB_bit == 3:
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 247) | binary_list[bit+3]#to take 4th number in binary list
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 251) | binary_list[bit+2]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 253) | binary_list[bit+1]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 254) | bit
    elif LSB_bit == 4:
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 239) | binary_list[bit+4]#to take 5th number in binary list
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 247) | binary_list[bit+3]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 251) | binary_list[bit+2]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 253) | binary_list[bit+1]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 254) | bit
    elif LSB_bit == 5:
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 223) | binary_list[bit+5]#to take 6th number in binary list
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 239) | binary_list[bit+4]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 247) | binary_list[bit+3]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 251) | binary_list[bit+2]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 253) | binary_list[bit+1]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 254) | bit
    elif LSB_bit == 6:
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 191) | binary_list[bit+6]#to take 7th number in binary list
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 223) | binary_list[bit+5]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 239) | binary_list[bit+4]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 247) | binary_list[bit+3]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 251) | binary_list[bit+2]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 253) | binary_list[bit+1]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 254) | bit
    elif LSB_bit == 7:
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 127) | binary_list[bit+7]#to take 8th number in binary list
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 191) | binary_list[bit+6]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 223) | binary_list[bit+5]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 239) | binary_list[bit+4]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 247) | binary_list[bit+3]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 251) | binary_list[bit+2]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 253) | binary_list[bit+1]
        for i, bit in enumerate(binary_list):
            audio_bytearray[i] = (audio_bytearray[i] & 254) | bit
    #Get the replaced bytes
    frame_replaced = bytes(audio_bytearray)
    
    #Writing bytes to a new wave audio file, can use mp3 too
    path=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop
    name = 'audio_encoded.wav'
    path = ''.join(path)
    with wave.open(join(path, name), 'wb') as fd:
        fd.setparams(cover_audio.getparams())
        fd.writeframes(frame_replaced)
    cover_audio.close()
    output_path = join(path, name)
    return(output_path)

def decoding_audio(audio_path,LSB_bit):
    embedded_audio = wave.open(audio_path, mode='rb')
    #Reading frames and converting it to byte array
    audio_bytearray = bytearray(list(embedded_audio.readframes(embedded_audio.getnframes())))

    if LSB_bit == 0:
        # Extract LSB of each byte
        extracted_LSB = [audio_bytearray[i] & 1 for i in range(len(audio_bytearray))]
    elif LSB_bit == 1:
        extracted_LSB = [(audio_bytearray[i] >> 1) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [audio_bytearray[i] & 1 for i in range(len(audio_bytearray))]
    elif LSB_bit == 2:
        extracted_LSB = [(audio_bytearray[i] >> 2) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 1) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [audio_bytearray[i] & 1 for i in range(len(audio_bytearray))]
    elif LSB_bit == 3:
        extracted_LSB = [(audio_bytearray[i] >> 3) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 2) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 1) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [audio_bytearray[i] & 1 for i in range(len(audio_bytearray))]
    elif LSB_bit == 4:
        extracted_LSB = [(audio_bytearray[i] >> 4) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 3) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 2) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 1) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [audio_bytearray[i] & 1 for i in range(len(audio_bytearray))]
    elif LSB_bit == 5:
        extracted_LSB = [(audio_bytearray[i] >> 5) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 4) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 3) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 2) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 1) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [audio_bytearray[i] & 1 for i in range(len(audio_bytearray))]
    elif LSB_bit == 6:
        extracted_LSB = [(audio_bytearray[i] >> 6) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 5) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 4) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 3) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 2) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 1) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [audio_bytearray[i] & 1 for i in range(len(audio_bytearray))]
    if LSB_bit == 7:
        extracted_LSB = [(audio_bytearray[i] >> 7) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 6) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 5) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 4) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 3) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 2) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [(audio_bytearray[i] >> 1) & 1 for i in range(len(audio_bytearray))]
        extracted_LSB = [audio_bytearray[i] & 1 for i in range(len(audio_bytearray))]
    
    #Convert byte array back to string
    embedded_text = "".join(chr(int("".join(map(str,extracted_LSB[i:i+8])),2)) for i in range(0,len(extracted_LSB),8))
    #Cut off at the filler characters
    decoded_text = embedded_text.split("###")[0]
    print("You encoded with " , LSB_bit , " and it works..... bitch")
    # Print the extracted text
    print("Payload is: "+decoded_text)
    embedded_audio.close()
    return decoded_text

# data = "input.xls"
# convert_to_txt(file_type(data),data)
# payload = "payload.txt"
# audio_file = "song_embedded.mp3"
# LSB_bit = int(input("Choose how many LSB bitch"))
# encoding(payload,audio_file,LSB_bit)
# decoding(LSB_bit)
