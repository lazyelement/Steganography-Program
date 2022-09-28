
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from asyncio.windows_events import ERROR_CONNECTION_ABORTED
from distutils.util import convert_path
from pathlib import Path
from pickle import GLOBAL
from re import I

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog
from tkinter import *
import tkinter as tk
from turtle import bgcolor
from PIL import Image, ImageTk
# from TkinterDnD2 import DND_FILES, TkinterDnD #need pip install
import time
import tkinterdnd2
import os
import docx2txt # pip install docx2txt
from tkinter.filedialog import askopenfile
from tkVideoPlayer import TkinterVideo # pip install tkvideoplayer
#from TkinterDnD2 import DND_FILES, TkinterDnD
import pygame   #pip install pygame

from text2textSteg import *
from LSBaudio_modify import *

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets") 

payload_flag = 0
cover_object_flag = 0
stego_flag = 0
payload_path = ""
cover_path = ""
stego_path = ""
output_path = ""
audio_paused_cover = False
audio_paused_payload = False
audio_paused_stego = False
audio_paused_output = False
textbox_choice = "Cover Object"
inputValue_payload = ""
inputValue_cover = ""
selectedLSB = 0


#init audio player
pygame.mixer.init()                     
#Set each audio channel for the various objects, so they can play/pause individually
cover_audio = pygame.mixer.Channel(0)
payload_audio = pygame.mixer.Channel(1)
stego_audio = pygame.mixer.Channel(2)
output_audio = pygame.mixer.Channel(3)


def vp_start_gui():
    global window
 
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # encode process
    def encode_process():
        global cover_path
        global payload_path
        global output_path
        global inputValue_cover
        global inputValue_payload
        global selectedLSB
        changeStateButton()
        if(payload_flag == 1 and cover_object_flag == 1):
            #create output box
            tbox_output = tk.Text(window, background="#ffffff")
            tbox_output.place(x=70,y=359,width=(471-70),height=(712-359))
            # text as cover & payload
            if(cover_path.endswith(".txt") and payload_path.endswith(".txt")):
                with open(cover_path, encoding="utf8", errors='ignore') as file:
                    for line in file:
                            cover = line.strip()
                with open(payload_path, encoding="utf8", errors='ignore') as file:
                    for line in file:
                            payload = line.strip()
                # do encoding show encoded text in output box
                encodedText = encode(cover,payload,selectedLSB)
                tbox_output.insert("end", encodedText)
                # save output into textfile
                saveTxtToFile(encodedText,"encodedText")
                tk.messagebox.showinfo(title="Success!", message="Encoding successful! Output saved as encodedText.txt") # Success message pop up
            # text for payload and cover but both user input    
            if(cover_path == "" and payload_path == ""):
                # do encoding show encoded text in output box
                encodedText = encode(inputValue_cover,inputValue_payload,selectedLSB)
                tbox_output.insert("end", encodedText)
                 # save output into textfile
                saveTxtToFile(encodedText,"encodedText")
                tk.messagebox.showinfo(title="Success!", message="Encoding successful! Output saved as encodedText.txt") # Success message pop up
            # Payload is anything. cover is audio
            if(cover_path.endswith(".wav") or cover_path.endswith(".mp3")):
                if(payload_path == ""): #using input typed in from user
                    output_path = encoding_audio(inputValue_payload,cover_path,selectedLSB)
                    previewSound(output_path, 3)
                else:
                    output_path = encoding_audio(payload_path,cover_path,selectedLSB)
                    previewSound(output_path, 3)
                tk.messagebox.showinfo(title="Success!", message="Encoding successful! Output saved as audio_encoded.wav") # Success message pop up
        elif(payload_flag == 1 and cover_object_flag == 0):
            tk.messagebox.showerror(title="Failed to encode", message="Encoding unsuccessful. Cover object missing.") # Error message pop up
        elif(payload_flag == 0 and cover_object_flag == 1):
            tk.messagebox.showerror(title="Failed to encode", message="Encoding unsuccessful. Payload missing.") # Error message pop up
        else:
            tk.messagebox.showerror(title="Failed to encode", message="Encoding unsuccessful. Payload and cover object missing.") # Error message pop up
        changeStateButton()

    def decode_process():
        global stego_path
        global selectedLSB
        changeStateButton()
        if(stego_flag == 1):
            if(stego_path.endswith(".txt")):
                with open(stego_path, encoding="utf8", errors='ignore') as file:
                    for line in file:
                            stego = line.strip()
                secret_text = decode(stego,selectedLSB)
                #output is in text form but not in a txt file
                tbox_output = tk.Text(window, background="#ffffff")
                tbox_output.place(x=70,y=359,width=(471-70),height=(712-359))
                tbox_output.insert("end", secret_text)
            if(stego_path.endswith(".wav")):
                secret_text = decoding_audio(stego_path,selectedLSB)
                #output is in text form but not in a txt file
                tbox_output = tk.Text(window, background="#ffffff")
                tbox_output.place(x=70,y=359,width=(471-70),height=(712-359))
                tbox_output.insert("end", secret_text)
                if(secret_text.endswith(".png")): #if secret is an image
                    previewImage(secret_text,3)
            tk.messagebox.showinfo(title="Success!", message="Decoding successful!") # Success message pop up
             
        else:
            tk.messagebox.showerror(title="Failed to decode", message="Decoding unsuccessful. Stego object missing.") # Error message pop up
        changeStateButton()

    # change button to disabled when loading
    def changeStateButton():
        if (decode_button['state'] == NORMAL):
            decode_button['state'] = DISABLED
        else:
            decode_button['state'] = NORMAL
        if (encode_button['state'] == NORMAL):
            encode_button['state'] = DISABLED
        else:
            encode_button['state'] = NORMAL

        #This function is use to preview images:
        ##params {path - the file path to obtain image}
        ##params {objectFlag - 0 for cover Object, 1 for payload, 2 for stego, 3 for output}   
    def previewImage(path, objectFlag):
        #print("object flag: " + str(objectFlag))
        global i
        if (objectFlag == 0):
            #Creates a label to display image on
            raw_image_label = Label(window, text="Select Raw Image", height=(624-379), width=(279-56), relief="solid",bg="#FFFFFF")
            raw_image_label.place(x=379, y=56)
        elif (objectFlag == 1):
            #Creates a label to display image on
            raw_image_label = Label(window, text="Select Raw Image", height=(315-70), width=(279-56), relief="solid",bg="#FFFFFF")
            raw_image_label.place(x=70, y=56)
        elif (objectFlag == 2):
            #Creates a label to display image on
            raw_image_label = Label(window, text="Select Raw Image", height=(933-688), width=(279-56), relief="solid",bg="#FFFFFF")
            raw_image_label.place(x=688, y=56)
        elif (objectFlag == 3): #Use objectflag 3 to preview output objects
            #Creates a label to display image on
            raw_image_label = Label(window, text="Select Raw Image", height=(712-359), width=(471-70), relief="solid",bg="#FFFFFF")
            raw_image_label.place(x=70, y=359)
            #Open image -> calculate optimal size to resize -> resize
            selected_image = Image.open(path)
            max_width = (471-70)
            aspect_ratio = max_width / float(selected_image.size[0])
            max_height = int((float(selected_image.size[1]) * float(aspect_ratio)))
            selected_image = selected_image.resize((max_width, max_height), Image.ANTIALIAS)
            selected_image = ImageTk.PhotoImage(selected_image)
            #config the size of image to label (CHANGE the height and width below to alter the size)
            raw_image_label.config(image=selected_image, height=(712-359), width= (471-70))
            raw_image_label.image = selected_image
            return

        #Open image -> calculate optimal size to resize -> resize
        selected_image = Image.open(path)
        max_width = (279-30)
        aspect_ratio = max_width / float(selected_image.size[0])
        max_height = int((float(selected_image.size[1]) * float(aspect_ratio)))
        selected_image = selected_image.resize((max_width, max_height), Image.ANTIALIAS)
        selected_image = ImageTk.PhotoImage(selected_image)
        #config the size of image to label (CHANGE the height and width below to alter the size)
        raw_image_label.config(image=selected_image, height=(624-400), width= (279-30))
        raw_image_label.image = selected_image

        #This function is use to preview text:
        ##params {path - the file path to obtain image}
        ##params {objectFlag - 0 for cover Object, 1 for payload, 2 for stego, 3 for output}
    def previewText(path, objectFlag):
        if(objectFlag == 0):
            tbox_coverobj = tk.Text(window, background="#ffffff")
            tbox_coverobj.place(x=379,y=56,width=(279-30),height=(624-400))
            if path.endswith(".docx"):
                text = docx2txt.process(path)
                tbox_coverobj.insert(1.0,text)
            else:    
                with open(path, "r") as file:
                    for line in file:
                            line = line.strip()
                            tbox_coverobj.insert("end", f"{line}\n")
        elif(objectFlag == 1):
            tbox_payload = tk.Text(window, background="#ffffff")
            tbox_payload.place(x=70,y=56,width=(279-30),height=(624-400))
            if path.endswith(".docx"):
                text = docx2txt.process(path)
                tbox_payload.insert(1.0,text)
            else:    
                with open(path, "r") as file:
                    for line in file:
                            line = line.strip()
                            tbox_payload.insert("end", f"{line}\n")
        elif(objectFlag == 2):
            tbox_stego = tk.Text(window, background="#ffffff")
            tbox_stego.place(x=688,y=56,width=(279-30),height=(624-400))
            if path.endswith(".docx"):
                text = docx2txt.process(path)
                tbox_stego.insert(1.0,text)
            else:    
                with open(path, "r") as file:
                    for line in file:
                            line = line.strip()
                            tbox_stego.insert("end", f"{line}\n")
        elif(objectFlag == 3):
            tbox_output = tk.Text(window, background="#ffffff")
            tbox_output.place(x=70,y=359,width=(471-70),height=(712-359))
            if path.endswith(".docx"):
                text = docx2txt.process(path)
                tbox_output.insert(1.0,text)
            else:    
                with open(path, "r") as file:
                    for line in file:
                            line = line.strip()
                            tbox_output.insert("end", f"{line}\n")
    #This function is use to preview video:
    ##params {path - the file path to obtain image}
    ##params {objectFlag - 0 for cover Object, 1 for payload, 2 for stego, 3 for output}
    def previewVideo(path,objectFlag):
        if(objectFlag == 0):
            global videoplayer_coverobj
            videoplayer_coverobj = TkinterVideo(master=window, scaled=True)
            videoplayer_coverobj.load(r"{}".format(path))
            videoplayer_coverobj.place(x=379,y=56,width=(279-30),height=(624-400))
        elif(objectFlag == 1):
            global videoplayer_payload
            videoplayer_payload = TkinterVideo(master=window, scaled=True)
            videoplayer_payload.load(r"{}".format(path))
            videoplayer_payload.place(x=70,y=56,width=(279-30),height=(624-400))
        elif(objectFlag == 2):
            global videoplayer_stego
            videoplayer_stego = TkinterVideo(master=window, scaled=True)
            videoplayer_stego.load(r"{}".format(path))
            videoplayer_stego.place(x=688,y=56,width=(279-30),height=(624-400))
        elif(objectFlag == 3):
            global videoplayer_output
            videoplayer_output = TkinterVideo(master=window, scaled=True)
            videoplayer_output.load(r"{}".format(path))
            videoplayer_output.place(x=70,y=359,width=(471-70),height=(712-359))
    
    def previewSound(path, objectFlag):
        if(objectFlag == 0):
            cover_listb = tk.Listbox(window, selectmode=tk.SINGLE)
            cover_listb.place(x=379,y=56,width=(279-30),height=(624-400))
            cover_listb.insert("end", path)
        elif(objectFlag == 1):
            payload_listb = tk.Listbox(window, selectmode=tk.SINGLE)
            payload_listb.place(x=70,y=56,width=(279-30),height=(624-400))
            payload_listb.insert("end", path)
        elif(objectFlag == 2):
            stego_listb = tk.Listbox(window, selectmode=tk.SINGLE)
            stego_listb.place(x=688,y=56,width=(279-30),height=(624-400))
            stego_listb.insert("end", path)
        elif(objectFlag == 3):
            output_listb = tk.Listbox(window, selectmode=tk.SINGLE)
            output_listb.place(x=70,y=359,width=(471-70),height=(712-359))
            output_listb.insert("end", path)

    
            

    # Play video and audio for cover object
    def playAgain_coverobj():
        global videoplayer_coverobj
        global cover_path
        global audio_paused_cover
        global cover_audio
        print("coverpath is", cover_path)
        if(cover_path.endswith(".mp3") or cover_path.endswith(".wav") and audio_paused_cover == False): #if audio is unpaused, play it from the start if play button is hit
            audio = pygame.mixer.Sound(cover_path)
            cover_audio.play(audio, loops=0)
        elif(cover_path.endswith(".mp3") or cover_path.endswith(".wav") and audio_paused_cover == True): #if audio is paused, unpause it
            cover_audio.unpause()
            audio_paused_cover = False
        else:
            print("Playing video")
            videoplayer_coverobj.play()
    
    # Pause video and audio for cover object
    def pauseVideo_coverobj():
        global videoplayer_coverobj
        global cover_path
        global audio_paused_cover
        if(cover_path.endswith(".mp3") or cover_path.endswith(".wav")):
            audio_paused_cover = True
            cover_audio.pause()
        else:
            print("Pausing video")
            videoplayer_coverobj.pause()

    # Play video and audio for payload
    def playAgain_payload():
        global videoplayer_payload
        global payload_path
        global audio_paused_payload
        global payload_audio
        if(payload_path.endswith(".mp3") or payload_path.endswith(".wav") and audio_paused_payload == False):
            audio = pygame.mixer.Sound(payload_path)
            payload_audio.play(audio, loops=0)
        elif(payload_path.endswith(".mp3") or payload_path.endswith(".wav") and audio_paused_payload == True):
            payload_audio.unpause()
            audio_paused_payload = False
        else:
            print("Playing video")
            videoplayer_payload.play()
    
    # Pause video and audio for payload
    def pauseVideo_payload():
        global videoplayer_payload
        global payload_path
        global audio_paused_payload
        if(payload_path.endswith(".mp3") or payload_path.endswith(".wav")):
            audio_paused_payload = True
            payload_audio.pause()
        else:
            print("Pausing video")
            videoplayer_payload.pause()

    # Play video and audio for stego
    def playAgain_stego():
        global videoplayer_stego
        global stego_path
        global audio_paused_stego
        global stego_audio
        if(stego_path.endswith(".mp3") or stego_path.endswith(".wav") and audio_paused_stego == False):
            audio = pygame.mixer.Sound(stego_path)
            stego_audio.play(audio, loops=0)
        elif(stego_path.endswith(".mp3") or stego_path.endswith(".wav") and audio_paused_stego == True):
            stego_audio.unpause()
            audio_paused_stego = False
        else:
            print("Playing video")
            videoplayer_stego.play()
    
    # Pause video and audio for stego
    def pauseVideo_stego():
        global videoplayer_stego
        global stego_path
        global audio_paused_stego
        if(stego_path.endswith(".mp3") or stego_path.endswith(".wav")):
            audio_paused_stego = True
            stego_audio.pause()
        else:
            print("Pausing video")
            videoplayer_stego.pause()

    # Play video and audio for output
    def playAgain_output():
        global videoplayer_output
        global output_path
        global audio_paused_output
        global output_audio
        if(output_path.endswith(".mp3") or output_path.endswith(".wav") and audio_paused_output == False):
            audio = pygame.mixer.Sound(output_path)
            output_audio.play(audio, loops=0)
        elif(output_path.endswith(".mp3") or output_path.endswith(".wav") and audio_paused_output == True):
            output_audio.unpause()
            audio_paused_output = False
        else:
            print("Playing video")
            videoplayer_output.play()
    
    # Pause video and audio for output
    def pauseVideo_output():
        global videoplayer_output
        global output_path
        global audio_paused_output
        if(output_path.endswith(".mp3") or output_path.endswith(".wav")):
            audio_paused_output = True
            output_audio.pause()
        else:
            print("Pausing video")
            videoplayer_output.pause()

    #function to open file explorer (and selecting file in file explorer) for cover
    def open_file_explorer_cover():
        global cover_object_flag
        global cover_path
        rep = filedialog.askopenfilenames(
            parent=window,
            initialdir=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop in file explorer
            #initialfile='tmp',
            filetypes=[("All files", "*")]) 

        try:
            cover_path = rep[0]
            print(cover_path)
            if(cover_path.endswith(".png") or cover_path.endswith(".jpg") or cover_path.endswith(".bmp")):
                #Call function to preview image & change cover flag to 1
                previewImage(cover_path, 0)
                cover_object_flag = 1
            elif(cover_path.endswith(".txt") or cover_path.endswith(".docx") or cover_path.endswith(".xlsx") or cover_path.endswith(".pdf")):
                #Call function to preview text & change cover flag to 1
                previewText(cover_path, 0)
                cover_object_flag = 1
            elif(cover_path.endswith(".mp4") ):
                previewVideo(cover_path, 0)
                cover_object_flag = 1
            elif(cover_path.endswith(".mp3") or cover_path.endswith(".wav")):
                previewSound(cover_path, 0)
                cover_object_flag = 1

        except IndexError:
            tk.messagebox.showerror(title="No file selected", message="No file selected") # Error message pop up
        #to-do: except top show error if file type selected not supported

    #function to open file explorer (and selecting file in file explorer) for payload
    def open_file_explorer_payload():
        global payload_flag
        global payload_path
        rep = filedialog.askopenfilenames(
            parent=window,
            initialdir=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop in file explorer
            #initialfile='tmp',
            filetypes=[("All files", "*")])

        try:
            payload_path = rep[0]
            print(payload_path)
            if(payload_path.endswith(".png") or payload_path.endswith(".jpg") or payload_path.endswith(".bmp")):
                #Call function to preview image & change payload flag to 1
                previewImage(payload_path, 1)
                payload_flag = 1
            elif(payload_path.endswith(".txt") or payload_path.endswith(".docx") or payload_path.endswith(".xls")):
                #Call function to preview text & change cover flag to 1
                previewText(payload_path, 1)
                payload_flag = 1
            elif(payload_path.endswith(".mp4")):
                previewVideo(payload_path, 1)
                payload_flag = 1
            elif(payload_path.endswith(".mp3") or payload_path.endswith(".wav")):
                previewSound(payload_path, 1)
                payload_flag = 1

        except IndexError:
            tk.messagebox.showerror(title="No file selected", message="No file selected") # Error message pop up
        #to-do: except top show error if file type selected not supported

    #function to open file explorer (and selecting file in file explorer) for stego
    def open_file_explorer_stego():
        global stego_flag
        global stego_path
        rep = filedialog.askopenfilenames(
            parent=window,
            initialdir=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop in file explorer
            #initialfile='tmp',
            filetypes=[("All files", "*")])

        try:
            stego_path = rep[0]
            print(stego_path)
            if(stego_path.endswith(".png") or stego_path.endswith(".jpg") or stego_path.endswith(".bmp")):
                #Call function to preview image & change stego flag to 1
                previewImage(stego_path, 2)
                stego_flag = 1
            elif(stego_path.endswith(".txt") or stego_path.endswith(".docx") or stego_path.endswith(".xls")):
                #Call function to preview text & change cover flag to 1
                previewText(stego_path, 2)
                stego_flag = 1
            elif(stego_path.endswith(".mp4")):
                previewVideo(stego_path, 2)
                stego_flag = 1
            elif(stego_path.endswith(".mp3") or stego_path.endswith(".wav")):
                previewSound(stego_path,2)
                stego_flag = 1

        except IndexError:
            tk.messagebox.showerror(title="No file selected", message="No file selected") # Error message pop up
        #to-do: except top show error if file type selected not supported

    def show_selected_lsb(choice):
        global selectedLSB
        selectedLSB = int(var.get())

    def show_selected_option_textbox(choice):
        global textbox_choice
        textbox_choice = variable.get()

    #  get input for textbox & display
    def retrieve_input():
        global textbox_choice
        global cover_object_flag
        global payload_flag
        global payload_path
        global cover_path
        global inputValue_payload
        global inputValue_cover
        inputValue=entry_2.get()
        if(textbox_choice == "Cover Object"):
            tbox_coverobj = tk.Text(window, background="#ffffff")
            tbox_coverobj.place(x=379,y=56,width=(279-30),height=(624-400))
            tbox_coverobj.insert("end", inputValue)
            cover_object_flag = 1
            # path set to none incase user added something and changed to adding own input isntead
            cover_path = ""
            inputValue_cover = inputValue
        else:
            tbox_payload = tk.Text(window, background="#ffffff")
            tbox_payload.place(x=70,y=56,width=(279-30),height=(624-400))
            tbox_payload.insert("end", inputValue)
            payload_flag = 1
            # path set to none incase user added something and changed to adding own input isntead
            payload_path = ""
            inputValue_payload = inputValue

    # window = Tk()
    window = tkinterdnd2.Tk()
    window.title("Best stego encoder thing in the market")

    window.geometry("1004x796")
    window.configure(bg = "#FFFFFF")



    canvas = Canvas(
        window,
        bg = "#FFFFFF",
        height = 796,
        width = 1004,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )

    # "Payload" text
    canvas.place(x = 0, y = 0)
    canvas.create_text(
        150.0,
        25.0,
        anchor="nw",
        text="Payload",
        fill="#000066",
        font=("Inter Bold", 20 * -1)
    )

    # Output Rectangle
    canvas.create_rectangle(
        70.0,
        359.0,
        471.0,
        712.0,
        fill="#F5F5F5",
        outline="#000066")

    # "Output" text
    canvas.create_text(
        233.0,
        322.0,
        anchor="nw",
        text="Output",
        fill="#000066",
        font=("Inter Bold", 20 * -1)
    )

    # LSB Textbox
    canvas.create_text(
        532.0,
        359.0,
        anchor="nw",
        text="Select number of LSB (0 - 7)",
        fill="#000066",
        font=("Inter Regular", 14 * -1)
    )

    # Text input Textbox
    canvas.create_text(
    533.0,
    428.0,
    anchor="nw",
    text="Enter text for payload / cover object",
    fill="#000066",
    font=("Inter Regular", 14 * -1)
    )

    entry_2 = Entry(
        bd=0,
        bg="#D9D9D9",
        highlightthickness=0
    )
    entry_2.place(
        x=532.0,
        y=449.0,
        width=401.0,
        height=25.0
    )

    # "Cover" text
    canvas.create_text(
        445.0,
        25.0,
        anchor="nw",
        text="Cover Object",
        fill="#000066",
        font=("Inter Bold", 20 * -1)
    )

    # "Stego" text
    canvas.create_text(
        782.0,
        25.0,
        anchor="nw",
        text="Stego",
        fill="#000066",
        font=("Inter Bold", 20 * -1)
    )

    # Encode Button
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    encode_button = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: encode_process(),
        relief="flat"
    )
    encode_button.place(
        x=535.0,
        y=586.0,
        width=155.0,
        height=70.0
    )

    # Create Dropdown for LSB
    OPTIONS = [i for i in range(0,8)]
    var = StringVar(window)
    var.set(OPTIONS[0]) # default value
    lsb_dropdown = OptionMenu(window, var, *OPTIONS,command=show_selected_lsb)
    lsb_dropdown.place(
        x=533.0,
        y=387.0
    )

    # Create Dropdown for textbox
    OPTIONS = ["Payload","Cover Object"]
    variable = StringVar(window)
    variable.set(OPTIONS[1]) # default value
    lsb_dropdown = OptionMenu(window, variable, *OPTIONS,command=show_selected_option_textbox)
    lsb_dropdown.place(
        x=760.0,
        y=480.0
    )

    # Decode button
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    decode_button = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: decode_process(),
        relief="flat"
    )
    decode_button.place(
        x=786.0,
        y=586.0,
        width=155.0,
        height=70.0
    )

    # Submit button
    button_image_15 = PhotoImage(
        file=relative_to_assets("button_13.png"))
    button_15 = Button(
        image=button_image_15,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: retrieve_input(),
        relief="flat"
    )
    button_15.place(
        x=880.0,
        y=480.0,
        width=55,
        height=30
    )

    # Payload Rectangle
    canvas.create_rectangle(
        70.0,
        56.0,
        315.0,
        279.0,
        fill="#F5F5F5",
        outline="#000066",
        dash=(4,4))

    # Payload rectangle text
    canvas.create_text(
        110.0,
        136.0,
        anchor="nw",
        text="Upload or drag and drop\n          your file here",
        fill="#000066",
        font=("Inter Regular", 14 * -1)
    )


    ################################################################################
    #Create an invisible canvas for Drag and drop for cover object
    cover_canvas = Canvas(window, width=(279-43),height=(624-412), relief='sunken', bg="#F5F5F5")
    cover_canvas.place(x=384,y=60)

    #define the drop event
    def cover_drop(event):
        global cover_object_flag
        global cover_path
        cover_path = event.data
        if(cover_path.endswith(".png") or cover_path.endswith(".jpg") or cover_path.endswith(".bmp")):
            previewImage(cover_path, 0)
            print(cover_path)
            cover_object_flag = 1
        elif(cover_path.endswith(".txt") or cover_path.endswith(".docx") or cover_path.endswith(".xls")):
            previewText(cover_path, 0)
            cover_object_flag = 1
        elif(cover_path.endswith(".mp4")):
            previewVideo(cover_path, 0)
            cover_object_flag = 1
        elif(cover_path.endswith(".mp3") or cover_path.endswith(".wav")):
                previewSound(cover_path, 0)
                cover_object_flag = 1

    cover_canvas.drop_target_register(tkinterdnd2.DND_FILES)
    cover_canvas.dnd_bind('<<Drop>>', cover_drop)

    # Cover rectangle
    canvas.create_rectangle(
        379.0,
        56.0,
        624.0,
        279.0,
        fill="#F5F5F5",
        outline="#000066",
        dash=(4,4))

    # Cover rectangle text
    cover_canvas.create_text(
        38.0,
        80.0,
        anchor="nw",
        text="Upload or drag and drop\n          your file here",
        fill="#000066",
        font=("Inter Regular", 14 * -1)
    )

    # Cover Browse button
    button_image_4 = PhotoImage(
        file=relative_to_assets("button_4.png"))
    cover_browse_button = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        highlightbackground='#000000',
        command=open_file_explorer_cover
    )
    cover_browse_button.place(
        x=535.0,
        y=288.0,
        width=93,
        height=28
    )


    ##################################################################################
    #Create an invisible canvas for Drag and drop for stego
    stego_canvas = Canvas(window, width=(279-43),height=(624-412), relief='sunken', bg="#F5F5F5")
    stego_canvas.place(x=690,y=60)

    #define the drop event
    def stego_drop(event):
        global stego_flag
        global stego_path
        stego_path = event.data
        if(stego_path.endswith(".png") or stego_path.endswith(".jpg") or stego_path.endswith(".bmp")):
            previewImage(stego_path, 2)
            stego_flag = 1
        elif(stego_path.endswith(".txt") or stego_path.endswith(".docx") or stego_path.endswith(".xls")):
            previewText(stego_path, 2)
            stego_flag = 1
        elif(stego_path.endswith(".mp4")):
            previewVideo(stego_path, 2)
            stego_flag = 1
        elif(stego_path.endswith(".mp3") or stego_path.endswith(".wav")):
            previewSound(stego_path, 2)
            stego_flag = 1
    stego_canvas.drop_target_register(tkinterdnd2.DND_FILES)
    stego_canvas.dnd_bind('<<Drop>>', stego_drop)


    # Stego Rectangle
    canvas.create_rectangle(
        688.0,
        56.0,
        933.0,
        279.0,
        fill="#F5F5F5",
        outline="#000066",
        dash=(4,4))

    # Stego rectangle text
    stego_canvas.create_text(
        38.0,
        80.0,
        anchor="nw",
        text="Upload or drag and drop\n          your file here",
        fill="#000066",
        font=("Inter Regular", 14 * -1)
    )

    # Stego browse button
    button_image_5 = PhotoImage(
        file=relative_to_assets("button_5.png"))
    stego_browse_button = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        activeforeground="#000066",
        command=open_file_explorer_stego
    )
    stego_browse_button.place(
        x=844.0,
        y=288.0,
        width=93,
        height=28
    )

    #############################################################################3
    #Create an invisible canvas for Drag and drop for payload
    payload_canvas = Canvas(window, width=(279-43),height=(624-412), relief='sunken', bg="#F5F5F5")
    payload_canvas.place(x=74,y=60)

    #define the drop event
    def payload_drop(event):
        global payload_flag
        global payload_path
        payload_path = event.data
        if(payload_path.endswith(".png") or payload_path.endswith(".jpg") or payload_path.endswith(".bmp")):
            previewImage(payload_path, 1)
            payload_flag = 1
        elif(payload_path.endswith(".txt") or payload_path.endswith(".docx") or payload_path.endswith(".xls")):
            previewText(payload_path, 1)
            payload_flag = 1
        elif(payload_path.endswith(".mp4")):
            previewVideo(payload_path, 1)
            payload_flag = 1
        elif(payload_path.endswith(".mp3") or payload_path.endswith(".wav")):
            previewSound(payload_path, 1)
            payload_flag = 1
    payload_canvas.drop_target_register(tkinterdnd2.DND_FILES)
    payload_canvas.dnd_bind('<<Drop>>', payload_drop)

    # payload rectangle
    canvas.create_rectangle(
        379.0,
        56.0,
        624.0,
        279.0,
        fill="#F5F5F5",
        outline="#000066",
        dash=(4,4))

    # payload rectangle text
    payload_canvas.create_text(
        38.0,
        80.0,
        anchor="nw",
        text="Upload or drag and drop\n          your file here",
        fill="#000066",
        font=("Inter Regular", 14 * -1)
    )

    # Payload Browse button
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    payload_browse_button = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=open_file_explorer_payload
    )
    payload_browse_button.place(
        x=226.0,
        y=288.0,
        width=93,
        height=28
    )

    # Reset button
    button_image_6 = PhotoImage(
        file=relative_to_assets("button_6.png"))
    reset_button = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: refresh(),
        relief="flat"
    )
    reset_button.place(
        x=836.0,
        y=671.0,
        width=103.0,
        height=41.0
    )
    
    # Stego play pause buttons
    button_image_7 = PhotoImage(
        file=relative_to_assets("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: playAgain_stego(),
        relief="flat"
    )
    button_7.place(
        x=689.0,
        y=285.0,
        width=24.0,
        height=24.0
    )

    button_image_8 = PhotoImage(
        file=relative_to_assets("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: pauseVideo_stego(),
        relief="flat"
    )
    button_8.place(
        x=720.0,
        y=285.0,
        width=24.0,
        height=24.0
    )

    # Payload play pause buttons
    button_image_9 = PhotoImage(
        file=relative_to_assets("button_9.png"))
    button_9 = Button(
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: playAgain_payload(),
        relief="flat"
    )
    button_9.place(
        x=70.0,
        y=286.0,
        width=24.0,
        height=24.0
    )

    button_image_10 = PhotoImage(
        file=relative_to_assets("button_10.png"))
    button_10 = Button(
        image=button_image_10,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: pauseVideo_payload(),
        relief="flat"
    )
    button_10.place(
        x=101.0,
        y=286.0,
        width=24.0,
        height=24.0
    )

    # Output play pause buttons
    button_image_13 = PhotoImage(
        file=relative_to_assets("button_9.png"))
    button_13 = Button(
        image=button_image_13,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: playAgain_output(),
        relief="flat"
    )
    button_13.place(
        x=70.0,
        y=718.0,
        width=24.0,
        height=24.0
    )

    button_image_14 = PhotoImage(
        file=relative_to_assets("button_10.png"))
    button_14 = Button(
        image=button_image_14,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: pauseVideo_output(),
        relief="flat"
    )
    button_14.place(
        x=101.0,
        y=718.0,
        width=24.0,
        height=24.0
    )

    # Cover object play pause buttons
    button_image_11 = PhotoImage(
        file=relative_to_assets("button_11.png"))
    button_11 = Button(
        image=button_image_11,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: playAgain_coverobj(),
        relief="flat"
    )
    button_11.place(
        x=380.0,
        y=286.0,
        width=24.0,
        height=24.0
    )

    button_image_12 = PhotoImage(
        file=relative_to_assets("button_12.png"))
    button_12 = Button(
        image=button_image_12,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: pauseVideo_coverobj(),
        relief="flat",
        #state=DISABLED
    )
    button_12.place(
        x=411.0,
        y=286.0,
        width=24.0,
        height=24.0
    )
    window.resizable(False, False)
    window.mainloop()

if __name__ == '__main__':
    def refresh():
        # Reset global flags & paths
        global payload_flag
        global cover_object_flag
        global stego_flag
        global payload_path
        global cover_path
        global stego_path
        global audio_paused_cover
        global audio_paused_payload
        global audio_paused_stego
        global audio_paused_output
        global textbox_choice
        global inputValue_cover
        global inputValue_payload
        global selectedLSB
        inputValue_payload = ""
        inputValue_cover = ""
        payload_flag = 0
        cover_object_flag = 0
        stego_flag = 0
        payload_path = ""
        cover_path = ""
        stego_path = ""
        audio_paused_cover = False
        audio_paused_payload = False
        audio_paused_stego = False
        audio_paused_output = False
        textbox_choice = "Cover Object"
        selectedLSB = 0

        # destroy window
        window.destroy()
        vp_start_gui()

    vp_start_gui()