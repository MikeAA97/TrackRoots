import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.image as mpimg
import numpy as np
from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label, regionprops
from skimage.morphology import closing, square
from skimage.color import label2rgb
from scipy.ndimage import label, generate_binary_structure
from tkinter import Tk
from pylab import imshow
from tkinter.filedialog import askopenfilename
from tkinter import *
from PIL import Image, ImageTk
import pandas as pd
import seaborn as sns

 #Plot the RGB image and save the plotted image as a JPG file which can be read into Tk.OpenImage Function
def toOrangeJPG(filePath):   #Read in filepath
   
    cutfile = filePath[:-3]   #Filename without the picture type(.bmp/.tif/jpg etc)
    fileJPG = (cutfile + "jpg")   #Add the JPG file type to original image path
    img = Image.open(filePath)     #Convert Filepath to image
    dataf = np.asarray(img)
    snsPlot = sns.heatmap(dataf, vmax=1000, cmap='Oranges', xticklabels=False, yticklabels=False, cbar=False)
    figure = snsPlot.get_figure()
    figure.set_size_inches(10,10)
    figure.savefig(fileJPG, dpi=100, bbox_inches='tight', pad_inches=0)
    
    return fileJPG

def toGreenJPG(filePath):   #Read in filepath
   
    cutfile = filePath[:-3]   #Filename without the picture type(.bmp/.tif/jpg etc)
    fileJPG = (cutfile + "jpg")   #Add the JPG file type to original image path
    img = Image.open(filePath)     #Convert Filepath to image
    dataf = np.asarray(img)
    snsPlot = sns.heatmap(dataf, vmax=1000, cmap='Greens', xticklabels=False, yticklabels=False, cbar=False)
    figure = snsPlot.get_figure()
    figure.set_size_inches(10,10)
    figure.savefig(fileJPG, dpi=100, bbox_inches='tight', pad_inches=0)
    
    return fileJPG
    
   

master = Tk()
#Set up initial image variables
imagePath1 = askopenfilename()
imagePath2 = askopenfilename()
 #Convert the images into a JPG for use in Tkinter window
image1 = Image.open(toGreenJPG(imagePath1))
image2 = Image.open(toOrangeJPG(imagePath2))
 #Set up structure for window
    
width = 1024
height = 1024  #Create an image object to initialize the size of the canvas window
 #Create the external windoww
 #Convert images from RGB to RGBA 
PREimg = image1.convert("RGBA")
PREimg2 = image2.convert("RGBA")
PREimg.putalpha(255)
PREimg2.putalpha(128)
print(PREimg.size)
print(PREimg2.size)
 #Merge the two images
c = Image.blend(PREimg, PREimg2, 0.42)
 #Counter for mouseclick events
count = 1
#Arrays to hold coordinate values and points
listOfXC = []
listOfYC = []
listOfP = []
listOfI = []
w = Canvas(master, width=width, height=height) #intialize the canvas on the external window with a size of the image being displayed
w.pack()
 #Plot the image
img1 = ImageTk.PhotoImage(PREimg)
img2 = ImageTk.PhotoImage(PREimg2)
w.create_image(0,0,anchor="nw",image=img1)
w.create_image(0,0,anchor="nw",image=img2)
#w.create_image(20,20,anchor="nw",image=img2)
#Create a function that plots a point and coordinates on the image




            
def click(event, x, y):
    xcoor = event.x
    ycoor = event.y

    
    def clickAndPrint(x, y):
        #outputting x and y coords to console
        global count
        global listOfXC
        global listOfYC     
        global listOfP
        global listOfI
        global PREimg2
        #imgData = np.asarray(PREimg2)
        #imgDS = imgData[:,:,0]
        pos = ("Point " + str(count))
        listOfP.append(pos)
        x, y = xcoor, ycoor
        listOfXC.append(x)
        listOfYC.append(y)
        print (pos, "coordinates are: ", str(x),",",str(y))
        w.create_oval(x-3,y-3, x+3, y+3, fill="yellow")
        if(count > -1):
            w.create_text(x+20,y-5,text=("Point " + str(count)))
            count +=1
        
    clickAndPrint(xcoor, ycoor) 
        
    
            
         
        
        
     #mouseclick event

w.bind("<Button 1>",click)
master.mainloop()
dataf = {'X Coordinates':listOfXC,'Y Coordinates':listOfYC}
df = pd.DataFrame(dataf, index=listOfP)
print(df)
df.to_csv("Test.csv")