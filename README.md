# ACW1.0_Steganography

## What is Steganography?
> Steganography is the practice of concealing a message within another message or a physical object. In computing/electronic contexts, a computer file, message, image, or video is concealed within another file, message, image, or video.

Basically, Steganography allows you to hide any type of message or data within another file without the file changing completely. You could hide an excel sheet within an image file and no one will be able to tell there is a hidden excel file in said image.

## 1. Program Overview 
This is a Steganography program that enables users to hide their data within different file types and vice versa. The program utilises the LSB Replacement algorithm and users are able to customize the number of bits they would like to use to hide their data (1-8 bits). Users are able to encode and decode their files with their respective bits selection. 

## 2. Features

### *File Upload*
The program provides two ways to upload files for encoding or decoding. 

#### 1. Drag and Drop
Users are able to drag and drop their files from anywhere on their desktop directly into our program

https://user-images.githubusercontent.com/93068145/194688013-9ee7a079-cffc-46f9-9e7e-aa7b83615283.mov


#### 2. Browse Files
Users are able to browse their computer directories to search for their files to upload into the program

https://user-images.githubusercontent.com/93068145/194688017-a244ac33-5128-4ed3-be19-7b1f5398068a.mov


### *Visual Preview*
The program is able to preview files that the users have uploaded/encoded/decoded. Image and Document file types are automatically shown to the users while Video and Audio file types have a play button for the users to preview the respective files.

https://user-images.githubusercontent.com/93068145/194688022-43c61e48-abaf-474f-9017-769f7e1a9a48.mov



### *Encoding*
Users are able to encode any file type whether it is an audio, video, image, text, excel, document, into any of the following file types: 

- Image (png, jpg, bmp)
- Video (avi, mp4, mpeg, mov, mkv)
- Audio (wav, mp3)
- Document (txt)

They are also able to select the number of bits they would like the algorithm to use for their encoding. 

Let's try an example. We will be encoding the following image

![small](https://user-images.githubusercontent.com/93068145/194687381-1a8e4c6f-fb40-45bc-be42-3cd389ec4c3e.jpg)

into the following video

https://user-images.githubusercontent.com/93068145/194687401-22af0ede-86cd-4386-b05c-6ce70c0101ed.mp4

The following video shows the program encoding our image into the video we have selected. We also use the option of 2 bits to hide our image data into the video.

https://user-images.githubusercontent.com/93068145/194687605-4115ad6e-c96b-4c29-8c3b-e2c7bdefdc8e.mov

Just for a reference, here are the two videos before and after encoding for a side-by-side comparison.

Original Video
https://user-images.githubusercontent.com/93068145/194687841-7e619211-ba80-418d-939f-b5ae940fa9e7.mp4

Video holding image inside
https://user-images.githubusercontent.com/93068145/194687926-d8a5f533-79f5-41f8-bcbf-a078f6ed4169.mp4


### *Decoding*
Users are able to decode any files that have been encoded by the program. Decoding process accepts an encoded file and the number of bits that was used to encode the file. Using these two information the program decodes the given file and outputs the hidden file/data within the encoded file.

We will be using the encoded video from above to retrieve the image hidden within.

https://user-images.githubusercontent.com/93068145/194687987-8f18ce97-5e93-451e-9e47-c812b76b02df.mov


### *Error Handling*
Sample Text

## 3. Installation Guide
Sample text


