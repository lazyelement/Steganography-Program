
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from asyncio.windows_events import ERROR_CONNECTION_ABORTED
from distutils.util import convert_path
from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog
from tkinter import *
import tkinter as tk
from turtle import bgcolor
from PIL import Image, ImageTk
# from TkinterDnD2 import DND_FILES, TkinterDnD #need pip install
import tkinterdnd2
import os
#from TkinterDnD2 import DND_FILES, TkinterDnD

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets") 

payload_flag = 0
cover_object_flag = 0
stego_flag = 0
payload_path = ""
cover_path = ""
stego_path = ""


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def encoder_check_for_error():
    if(payload_flag == 1 and cover_object_flag == 1):
        tk.messagebox.showinfo(title="Success!", message="Encoding successful!") # Success message pop up
    elif (payload_flag == 1 and cover_object_flag == 0):
        tk.messagebox.showerror(title="Failed to encode", message="Encoding unsuccessful. Cover object missing.") # Error message pop up
    elif (payload_flag == 0 and cover_object_flag == 1):
        tk.messagebox.showerror(title="Failed to encode", message="Encoding unsuccessful. Payload missing.") # Error message pop up
    else:
        tk.messagebox.showerror(title="Failed to encode", message="Encoding unsuccessful. Payload and cover object missing.") # Error message pop up
    

def decoder_check_for_error():
    if(stego_flag == 1):
        tk.messagebox.showinfo(title="Success!", message="Decoding successful!") # Success message pop up
    else:
        tk.messagebox.showerror(title="Failed to decode", message="Decoding unsuccessful. Stego object missing.") # Error message pop up

    #This function is use to preview images:
    ##params {path - the file path to obtain image}
    ##params {objectFlag - 0 for cover Object, 1 for payload, 2 for stego, 3 for output}   
def previewImage(path, objectFlag):
    if (objectFlag == 0):
        #Creates a label to display image on
        raw_image_label = Label(window, text="Select Raw Image", height=(624-379), width=(279-56), relief="solid",bg="#FFFFFF")
        raw_image_label.place(x=379, y=56)
        #Open image -> calculate optimal size to resize -> resize
        selected_image = Image.open(path)
        max_width = (279-56)
        aspect_ratio = max_width / float(selected_image.size[0])
        max_height = int((float(selected_image.size[1]) * float(aspect_ratio)))
        selected_image = selected_image.resize((max_width, max_height), Image.ANTIALIAS)
        selected_image = ImageTk.PhotoImage(selected_image)
        #config the size of image to label (CHANGE the height and width below to alter the size)
        raw_image_label.config(image=selected_image, height=(624-402), width= (279-38))
        raw_image_label.image = selected_image
    elif (objectFlag == 1):
        #Creates a label to display image on
        raw_image_label = Label(window, text="Select Raw Image", height=(315-70), width=(279-56), relief="solid",bg="#FFFFFF")
        raw_image_label.place(x=70, y=56)
        #Open image -> calculate optimal size to resize -> resize
        selected_image = Image.open(path)
        max_width = (279-56)
        aspect_ratio = max_width / float(selected_image.size[0])
        max_height = int((float(selected_image.size[1]) * float(aspect_ratio)))
        selected_image = selected_image.resize((max_width, max_height), Image.ANTIALIAS)
        selected_image = ImageTk.PhotoImage(selected_image)
        #config the size of image to label (CHANGE the height and width below to alter the size)
        raw_image_label.config(image=selected_image, height=(624-402), width= (279-38))
        raw_image_label.image = selected_image
    elif (objectFlag == 2):
        #Creates a label to display image on
        raw_image_label = Label(window, text="Select Raw Image", height=(933-688), width=(279-56), relief="solid",bg="#FFFFFF")
        raw_image_label.place(x=688, y=56)
        #Open image -> calculate optimal size to resize -> resize
        selected_image = Image.open(path)
        max_width = (279-56)
        aspect_ratio = max_width / float(selected_image.size[0])
        max_height = int((float(selected_image.size[1]) * float(aspect_ratio)))
        selected_image = selected_image.resize((max_width, max_height), Image.ANTIALIAS)
        selected_image = ImageTk.PhotoImage(selected_image)
        #config the size of image to label (CHANGE the height and width below to alter the size)
        raw_image_label.config(image=selected_image, height=(624-402), width= (279-38))
        raw_image_label.image = selected_image
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


    #This function is use to preview text:
    ##params {path - the file path to obtain image}
    ##params {objectFlag - 0 for cover Object, 1 for payload, 2 for stego, 3 for output}
def previewText(path, objectFlag):
    if(objectFlag == 0):
        tbox_coverobj = tk.Text(window, background="#ffffff")
        tbox_coverobj.place(x=379,y=56,width=(279-30),height=(624-400))
        with open(path, "r") as file:
            for line in file:
                    line = line.strip()
                    tbox_coverobj.insert("end", f"{line}\n")
    elif(objectFlag == 1):
        tbox_payload = tk.Text(window, background="#ffffff")
        tbox_payload.place(x=70,y=56,width=(279-30),height=(624-400))
        with open(path, "r") as file:
            for line in file:
                    line = line.strip()
                    tbox_payload.insert("end", f"{line}\n")
    elif(objectFlag == 2):
        tbox_payload = tk.Text(window, background="#ffffff")
        tbox_payload.place(x=688,y=56,width=(279-30),height=(624-400))
        with open(path, "r") as file:
            for line in file:
                    line = line.strip()
                    tbox_payload.insert("end", f"{line}\n")
    elif(objectFlag == 3):
        tbox_output = tk.Text(window, background="#ffffff")
        tbox_output.place(x=70,y=359,width=(471-70),height=(712-359))
        with open(path, "r") as file:
            for line in file:
                    line = line.strip()
                    tbox_output.insert("end", f"{line}\n")



    

def previewVideo(path):
    videoplayer = TkinterVideo(master=window, scaled=True)
    videoplayer.load(path)
    videoplayer.pack(expand=True, fill="both")
    videoplayer.play()

#function to open file explorer (and selecting file in file explorer) for cover
def open_file_explorer_cover():
    rep = filedialog.askopenfilenames(
    	parent=window,
    	initialdir=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop in file explorer
    	#initialfile='tmp',
    	filetypes=[("All files", "*")])

    try:
        cover_path = rep[0]
        print(cover_path)
        if(cover_path.endswith(".png")):
            #Call function to preview image & change cover flag to 1
            previewImage(cover_path, 0)
            cover_object_flag = 1
        elif(cover_path.endswith(".txt")):
            #Call function to preview text & change cover flag to 1
            previewText(cover_path,0)
            cover_object_flag = 1
        elif(cover_path.endswith(".mp4")):
            previewVideo(cover_path)
            cover_object_flag = 1

    except IndexError:
        tk.messagebox.showerror(title="No file selected", message="No file selected") # Error message pop up
     #to-do: except top show error if file type selected not supported

#function to open file explorer (and selecting file in file explorer) for payload
def open_file_explorer_payload():
    rep = filedialog.askopenfilenames(
    	parent=window,
    	initialdir=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop in file explorer
    	#initialfile='tmp',
    	filetypes=[("All files", "*")])

    try:
        payload_path = rep[0]
        print(payload_path)
        if(payload_path.endswith(".png")):
            #Call function to preview image & change payload flag to 1
            previewImage(payload_path, 1)
            payload_flag = 1
        elif(payload_path.endswith(".txt")):
            #Call function to preview text & change cover flag to 1
            previewText(payload_path, 1)
            payload_flag = 1
        elif(payload_path.endswith(".mp4")):
            previewVideo(payload_path)
            payload_flag = 1

    except IndexError:
        tk.messagebox.showerror(title="No file selected", message="No file selected") # Error message pop up
     #to-do: except top show error if file type selected not supported

#function to open file explorer (and selecting file in file explorer) for stego
def open_file_explorer_stego():
    rep = filedialog.askopenfilenames(
    	parent=window,
    	initialdir=os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop'), # set path to open desktop in file explorer
    	#initialfile='tmp',
    	filetypes=[("All files", "*")])

    try:
        stego_path = rep[0]
        print(stego_path)
        if(stego_path.endswith(".png")):
            #Call function to preview image & change stego flag to 1
            previewImage(stego_path, 2)
            stego_flag = 1
        elif(stego_path.endswith(".txt")):
            #Call function to preview text & change cover flag to 1
            previewText(stego_path, 2)
            stego_flag = 1
        elif(stego_path.endswith(".mp4")):
            previewVideo(stego_path)
            stego_flag = 1

    except IndexError:
        tk.messagebox.showerror(title="No file selected", message="No file selected") # Error message pop up
     #to-do: except top show error if file type selected not supported

def show_selected_lsb(choice):
    choice = variable.get()
    print("Option selected: "+choice)


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
    command=lambda: encoder_check_for_error(),
    relief="flat"
)
encode_button.place(
    x=532.0,
    y=651.0,
    width=155.0,
    height=70.0
)

# # Textbox image for LSB
# entry_image_1 = PhotoImage(
#     file=relative_to_assets("entry_1.png"))
# entry_bg_1 = canvas.create_image(
#     696.5,
#     398.0,
#     image=entry_image_1
# )
# entry_1 = Entry(
#     bd=0,
#     bg="#D9D9D9",
#     highlightthickness=0
# )
# entry_1.place(
#     x=533.0,
#     y=387.0,
#     width=327.0,
#     height=20.0
# )

# Create Dropdown
OPTIONS = ["0","1","2","3","4","5","6","7"]
variable = StringVar(window)
variable.set(OPTIONS[0]) # default value
lsb_dropdown = OptionMenu(window, variable, *OPTIONS,command=show_selected_lsb)
lsb_dropdown.place(
     x=533.0,
     y=387.0
)

# Decode button
button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
decode_button = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: decoder_check_for_error(),
    relief="flat"
)
decode_button.place(
    x=772.0,
    y=651.0,
    width=155.0,
    height=70.0
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
    x=146.0,
    y=215.0,
    width=95,
    height=30
)
################################################################################

#Create an invisible canvas for Drag and drop
cover_canvas = Canvas(window, width=(279-43),height=(624-412), relief='sunken', bg="#F5F5F5")
cover_canvas.place(x=384,y=60)

#define the drop evnt
def cover_drop(event):
    cover_path = event.data
    if(cover_path.endswith(".png")):
        previewImage(cover_path, 0)
        cover_object_flag = 1
    elif(cover_path.endswith(".txt")):
        previewText(cover_path, 0)
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
    command=open_file_explorer_cover
)
cover_browse_button.place(
    x=455.0,
    y=215.0,
    width=95,
    height=30
)


##################################################################################
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
canvas.create_text(
    727.0,
    136.0,
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
    x=764.0,
    y=215.0,
    width=95,
    height=30
)


window.resizable(False, False)
window.mainloop()
