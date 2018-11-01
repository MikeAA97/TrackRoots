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
    
#Create a function that plots a point and coordinates on the image  
def clickAndPrint(event):
    
    global count
    global listOfXC
    global listOfYC     
    global listOfP
    global listOfI
    global PREimg2
    global image2
    #outputting x and y coords to console
    pos = ("Point " + str(count))
    #add poistion to list
    listOfP.append(pos)
    #get coordinates on mouse click
    x = event.x
    y = event.y
    # add coordinates to lists
    listOfXC.append(x)
    listOfYC.append(y)
    
    #convert image to numpy array
    imgD = np.asarray(image2)
    imgDS = imgD[:,:,0]
    #get intensity from coordinate of mouseclick
    startIntensity = 249 #imgDS[y][x]
    listOfI.append(imgDS[y][x])
    print("starting intensity is ", str(startIntensity))
    print (pos, "coordinates are: ", str(x),",",str(y))
    #draw point 
    w.create_oval(x-3,y-3, x+3, y+3, fill="yellow")
    #add text to point
    if(count > -1):
        w.create_text(x+20,y-5,text=("Point " + str(count)))
        count +=1 
        
    ###Track root
    #Base Case
    b = 0
    r = isRoot(x,y,imgDS, startIntensity, b)
    #recursion
    while( r != ''):
        if(r=='left'):
            x-=1
            y+=1
            n = isRoot(x,y,imgDS,startIntensity, b)
        elif(r == 'right'):
            x+=1
            y+=1
            n = isRoot(x,y, imgDS, startIntensity, b)
        elif(r == 'down'):
            y+=2
            n = isRoot(x,y, imgDS, startIntensity,b)
        r = n

def isRoot(xcoor, ycoor, imgDS, startIntensity, buffer):
     #check left pixel
    global count
    checkNext = ''
    if imgDS[ycoor][xcoor-1] <= startIntensity+buffer:
        newx = xcoor-1
        pos = ("Point " + str(count))
        listOfP.append(pos)
        listOfXC.append(newx)
        listOfYC.append(ycoor)
        listOfI.append(imgDS[ycoor][newx])
        count +=1 
        print ("left coordinates are: ", str(newx),",",str(ycoor))
        w.create_oval(newx-3,ycoor-3, newx+3, ycoor+3, fill="yellow")
        #w.create_text(newx+20,ycoor-5,text=("added"))
        checkNext = 'left'
        return checkNext
    # check right pixel
    if imgDS[ycoor][xcoor+1] <= startIntensity+buffer:
        newx = xcoor+1
        pos = ("Point " + str(count))
        listOfP.append(pos)
        listOfXC.append(newx)
        listOfYC.append(ycoor)
        listOfI.append(imgDS[ycoor][newx])
        count +=1 
        print ("right coordinates are: ", str(newx),",",str(ycoor))
        w.create_oval(newx-3, ycoor-3, newx+3, ycoor+3, fill="yellow")
        #w.create_text(newx+20,ycoor-5,text=("added"))
        checkNext = 'right'
        return checkNext
    # check down pixel
    if imgDS[ycoor-1][xcoor] <= startIntensity+buffer:
        newy = ycoor + 1
        pos = ("Point " + str(count))
        listOfP.append(pos)
        listOfXC.append(xcoor)
        listOfYC.append(newy)
        listOfI.append(imgDS[newy][xcoor])
        count +=1 
        print ("down coordinates are: ", str(xcoor),",",str(newy))
        w.create_oval(xcoor-3,newy-3, xcoor+3, newy+3, fill="yellow")
        #w.create_text(xcoor+20,newy-5,text=("added"))
        checkNext = 'down'
        return checkNext
    else:
        print("Not Working") 
    # return what point to check next in recursion
    return checkNext
        

############################################################################

###-Run GUI
master = Tk()

#Set up initial image variables
imagePath1 = 'C:/Users/loves/OneDrive/Desktop/TrackRoots/071217-pos1,3-dr5;pos2,4-cle44-luc-1-5/pos1,3-dr5_pos2,4-cle44-luc-1-5_w1[None]_s1_t1.TIF' #askopenfilename()
imagePath2 = 'C:/Users/loves/OneDrive/Desktop/TrackRoots/071217-pos1,3-dr5;pos2,4-cle44-luc-1-5/pos1,3-dr5_pos2,4-cle44-luc-1-5_w1[None]_s1_t49.TIF' #askopenfilename()
#Convert the images into a JPG for use in Tkinter window
image1 = Image.open(toGreenJPG(imagePath1))
image2 = Image.open(toOrangeJPG(imagePath2))
# Window size
width = 1024
height = 1024 
#Convert images from RGB to RGBA 
PREimg = image1.convert("RGBA")
PREimg2 = image2.convert("RGBA")
#Set alpha valu for images such that the top one is more transparent
PREimg.putalpha(255)
PREimg2.putalpha(128)
# print(PREimg.size)
# print(PREimg2.size)


#Counter for mouseclick events
count = 1
#Arrays to hold coordinate values and points
listOfXC = []
listOfYC = []
listOfP = []
listOfI = []
#intialize the canvas on the external window with a size of the image being displayed
w = Canvas(master, width=width, height=height) 
w.pack()

#Plot the image
#converting image to TK image
img1 = ImageTk.PhotoImage(PREimg)
img2 = ImageTk.PhotoImage(PREimg2)
#putting TK images on canvas
w.create_image(0,0,anchor="nw",image=img1)
w.create_image(0,0,anchor="nw",image=img2)


#mouseclick event    
w.bind("<Button 1>",clickAndPrint)
#Ends GUI
master.mainloop()
#Output coords
dataf = {'X Coordinates':listOfXC,'Y Coordinates':listOfYC, 'Intensities':listOfI}
df = pd.DataFrame(dataf, index=listOfP)
print(df)
df.to_csv("Test.csv")