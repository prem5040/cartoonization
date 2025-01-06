from ctypes.wintypes import RGB
import cv2 #library to solve computer vision problems and tool for image processing
from matplotlib.colors import rgb2hex #To convert colors rgb to hex code
import numpy as np #performs mathematical operations on array
import matplotlib.pyplot as plt

import easygui #module for easy GUI programming
import imageio #provides interface to read images
import sys #provides function to manipulate different various runtime environment
import os# provides function for crating and removing directory fetching its contents
from PIL import ImageTk, Image

import tkinter as tk #provides fast and easy way to create GUI applications
from tkinter import filedialog # provides classes and function for creating file directory selection windows
from tkinter import *

top=tk.Tk()
top.geometry('400x450')
top.title('Cartoonize Avatar')
top.configure(background='lightblue')
label=Label(top,background='#CDCDCD', font=('verdana',22,'bold'))

def upload():
    ImagePath=easygui.fileopenbox()
    cartoonify(ImagePath)


def cartoonify(ImagePath):
    #Load Your Photo
    original = cv2.imread(ImagePath)
    original = cv2.cvtColor(original, cv2.COLOR_BGR2RGB)


    if original is None:
        print("Photo Not Uploaded !!! Try Again...")
        sys.exit()
    img1=original
    

    #transformation to grayscale
    gray=cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
    img2=gray

    linesize=7
    blurvalue=5
    #We have applied median blur to smoothen an image
    grayblur=cv2.medianBlur(gray,blurvalue)
    img3=grayblur

    #We have used thresold technique to retrieve edges for cartoon effect
    edges=cv2.adaptiveThreshold(grayblur,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY, linesize,blurvalue)
    img4 = edges
    #plt.imshow(original4, cmap='gray')

    data = np.float32(original).reshape((-1,3))
    k=9
    criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER,20,0.001)
    ret, label, center=cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    result=center[label.flatten()]
    result=result.reshape(original.shape)
    img5=result

    blurred=cv2.bilateralFilter(result,d=3, sigmaColor=200, sigmaSpace=200)
    img6=blurred

    c=cv2.bitwise_and(blurred, blurred, mask=edges)
    img7=c
    
    images=[img1, img2, img3, img4, img5, img6, img7]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 
    'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(top,text="Save cartoon image",command=lambda: save(img6, ImagePath),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)

    plt.show()
    
    
def save(img7, ImagePath):

    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(img7, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

upload=Button(top,text="Upload Your Photo",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='lightblue',font=('calibri',14,'bold'))
upload.pack(side=TOP,pady=50)

exitButton= Button(top,text="Exit Program", command=top.destroy)
exitButton.configure(background='black', foreground='lightblue', font=('calibri',12,'bold'))
exitButton.pack(side=BOTTOM, pady=50)

top.mainloop()
