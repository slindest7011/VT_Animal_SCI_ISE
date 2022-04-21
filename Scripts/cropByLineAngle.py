import cv2
import numpy as np
import imutils
import os
import pandas as pd
import keyboard 
import pyrealsense2 as rs
from numpy import ones,vstack
from numpy.linalg import lstsq
import math
import pickle

from sympy import true

def getHeight(depthBag, x, y):
    emptyScale = r"C:\Users\indes\PycharmProjects\VT_Animal_SCI_ISE\RealsenseCameraTriggers\FarmVisit7\FarmVisit7\cow#_15_FarmVisit6_pic_9__7372.bag"
    config = rs.config()
    config.enable_device_from_file(depthBag)
    config2 = rs.config()
    config2.enable_device_from_file(emptyScale)
    
    pipeline = rs.pipeline()
    pipeline.start(config)
    pipeline2 = rs.pipeline()
    pipeline2.start(config2)

    frame = pipeline.wait_for_frames()
    frame2 = pipeline2.wait_for_frames()
    #Retrieve the first depth frame, if no frame is found, return an empty frame instance.
    depth2, depth = frame2.get_depth_frame(), frame.get_depth_frame()
    print(x)
    print(y)
    value = depth2.get_distance(x,y) - depth.get_distance(x, y)
    
    print(value)
    return value



def getCowDim(Depth):
    #iterate over files in directory (inputFolder)
    #@param inputFolder must be directory containing only .png files

    cv2.imshow('Original Image', Depth)
    #crops image 
    #crop values should be set to inside of top rail 
    #this prevents errors in threshold seperation of rail
    Depth = Depth[180:485, 90:Depth.shape[1]] #image crop
    # Depth[200:510, 165:Depth.shape[1]] video crop
    #cv2.imshow('croped Image', Depth)
    #Convert RGB to HSV (Hue, Saturation, Value)
    hsvImage = cv2.cvtColor(Depth, cv2.COLOR_BGR2HSV)
    #show image (PRESS ANY KEY TO CONT)
    #cv2.imshow('HSV', hsvImage)
    #get h,s,v values
    h, s, v = hsvImage[:, :, 0], hsvImage[:, :, 1], hsvImage[:, :, 2]
    #creates a threshold using hue value
    (thresh, BW3) = cv2.threshold(h, 35, 255, cv2.THRESH_BINARY)
    #cv2.imshow('H_Black and white', BW3)
    # Remove stuructures connected to the image border------------------------------------------------
    # find contours in the image and initialize the mask that will be
    cnts = cv2.findContours(BW3.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    mask = np.ones( BW3.shape[:2], dtype="uint8") * 255

    ######################## Used for finding width and length of cow. Not used in this script ############################
    #draws a rectangle around largest contour
    


    im = Depth
    row, col = im.shape[:2]
    bottom = im[row-2:row, 0:col]
    mean = cv2.mean(bottom)[0]

    bordersize = 100
    border = cv2.copyMakeBorder(
        im,
        top=bordersize,
        bottom=bordersize,
        left=bordersize,
        right=bordersize,
        borderType=cv2.BORDER_CONSTANT,
        value=[mean, mean, mean]
    )


    c = max(cnts, key = cv2.contourArea)
    #c = cnts[]
    x,y,w,h = cv2.boundingRect(c) 
    #cv2.rectangle(Depth.copy(),(x,y),(x+w,y+h),(0,255,0),7)

   
    #print(c[0][0])
    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect) + 100
    box = np.int0(box)
    
    border2= border.copy()
    cv2.drawContours(border2,[box],0,(0,0,0),3)
    cv2.rectangle(border2,(x+bordersize,y+bordersize),(x+bordersize+w,y+bordersize+h),(0,255,0),3)
    cv2.imshow('border2',border2)
    cv2.waitKey()
    regRec = True
    if(keyboard.is_pressed('2')):
        regRec = False
    while not (keyboard.is_pressed('g') or keyboard.is_pressed('b')):

        if regRec:
            while keyboard.is_pressed('shift'):
                if keyboard.is_pressed('down'):
                    y=y+10
                    h=h-10
                if keyboard.is_pressed('up'):
                    h=h-10
                if keyboard.is_pressed('right'):
                    x=x+10
                    w=w-10
                if keyboard.is_pressed('left'):
                    w=w-10
                newRec = border.copy()
                cv2.rectangle(newRec,(x+bordersize,y+bordersize),(x+bordersize+w,y+bordersize+h),(0,0,0),3)
                cv2.imshow('movedRec',  newRec) 
                cv2.waitKey()
            if keyboard.is_pressed('down'):
                h=h+10
            if keyboard.is_pressed('up'):
                y=y-10
                h=h+10
            if keyboard.is_pressed('right'):
                w=w+10
            if keyboard.is_pressed('left'):
                x=x-10
                w=w+10
            newRec = border.copy()
            cv2.rectangle(newRec,(x+bordersize,y+bordersize),(x+bordersize+w,y+bordersize+h),(0,0,0),3)
            cv2.imshow('movedRec',  newRec) 
            cv2.waitKey()
        
        else:
            while keyboard.is_pressed('shift'):

                if keyboard.is_pressed('down'):
                    if(box[1][0] < box[3][0]):
                        #1 to 0 and 2 to 3
                    
                        a1 = math.atan2(box[0][1]-box[1][1], box[0][0]-box[1][0])
                        box[2][0] = box[2][0] - math.cos(a1) *10
                        box[2][1] = box[2][1] + math.sin(a1) *10
                        box[1][1] = box[1][1] + math.sin(a1) *10
                        box[1][0] = box[1][0] - math.cos(a1) *10
                    else:
                        #0 to 3 and 1 to 2
                  
                        a1 = math.atan2(box[3][1]-box[0][1], box[3][0]-box[0][0])
                        box[1][0] = box[1][0] + math.cos(a1) *10
                        box[1][1] = box[1][1] + math.sin(a1) *10
                        box[0][0] = box[0][0] + math.cos(a1) *10
                        box[0][1] = box[0][1] + math.sin(a1) *10

                if keyboard.is_pressed('up'):
                    if(box[1][0] < box[3][0]):
                        #0 to 1 and 3 to 2
                  
                        a1 = math.atan2(box[1][1]-box[0][1], box[1][0]-box[0][0])
                        a2 = math.atan2(box[2][1]-box[3][1], box[2][0]-box[3][0])
                        box[3][0] = box[3][0] + math.cos(a2) *10
                        box[3][1] = box[3][1] + math.sin(a2) *10
                        box[0][1] = box[0][1] + math.sin(a1) *10
                        box[0][0] = box[0][0] + math.cos(a1) *10
                    else:
                        #3 to 0 and 2 to 1
                       
                        a1 = math.atan2(box[0][1]-box[3][1], box[0][0]-box[3][0])
                        a2 = math.atan2(box[1][1]-box[2][1], box[1][0]-box[2][0])
                        box[2][0] = box[2][0] + math.cos(a2) *10
                        box[2][1] = box[2][1] + math.sin(a2) *10
                        box[3][0] = box[3][0] + math.cos(a1) *10
                        box[3][1] = box[3][1] + math.sin(a1) *10

                if keyboard.is_pressed('right'):
                    if(box[1][0] < box[3][0]):
                        #0 to 1 and 3 to 2
                      
                        a1 = math.atan2(box[2][1]-box[1][1], box[2][0]-box[1][0])
                        a2 = math.atan2(box[3][1]-box[0][1], box[3][0]-box[0][0])
                        box[1][0] = box[1][0] + math.cos(a1) *10
                        box[1][1] = box[1][1] + math.sin(a1) *10
                        box[0][1] = box[0][1] + math.sin(a2) *10
                        box[0][0] = box[0][0] + math.cos(a2) *10
                    else:
                        a1 = math.atan2(box[1][1]-box[0][1], box[1][0]-box[0][0])
                        print(a1)
                        box[0][0] = box[0][0] + math.cos(-a1) *10
                        box[0][1] = box[0][1] - math.sin(-a1) *10
                        box[3][0] = box[3][0] + math.cos(-a1) *10
                        box[3][1] = box[3][1] - math.sin(-a1) *10

                if keyboard.is_pressed('left'):
                    if(box[1][0] < box[3][0]):
                        a1 = math.atan2(box[2][1]-box[1][1], box[2][0]-box[1][0])
                        box[2][0] = box[2][0] - math.cos(a1) *10
                        box[2][1] = box[2][1] - math.sin(a1) *10
                        box[3][1] = box[3][1] - math.sin(a1) *10
                        box[3][0] = box[3][0] - math.cos(a1) *10
                    else:
                        #1 to 0 and 2 to 3
                        a1 = math.atan2(box[0][1]-box[1][1], box[0][0]-box[1][0])
                        box[1][0] = box[1][0] + math.cos(-a1) *10
                        box[1][1] = box[1][1] - math.sin(-a1) *10
                        box[2][0] = box[2][0] + math.cos(-a1) *10
                        box[2][1] = box[2][1] - math.sin(-a1) *10

                #Depth = Depth1[180:485, 90:Depth.shape[1]]
                newRec = border.copy()
                cv2.drawContours(newRec,[box],0,(0,0,0),3)
                cv2.imshow('movedRec',  newRec) 
                cv2.waitKey()
               # cv2.destroyAllWindows()
            if keyboard.is_pressed('up'):
                if(box[1][0] > box[3][0]): 
                    a1 = math.atan2(box[3][1]-box[0][1], box[3][0]-box[0][0])
                    a2 = math.atan2(box[2][1]-box[1][1], box[2][0]-box[1][0])
                    print(a2)
                    box[0][0] = box[0][0] - math.cos(a1) *10
                    box[0][1] = box[0][1] - math.sin(a1) *10
                    box[1][0] = box[1][0] - math.cos(a2) *10
                    box[1][1] = box[1][1] - math.sin(a2) *10
                else:
                    a1 =  math.atan2(box[1][1]-box[0][1], box[1][0]-box[0][0])
    
                    box[2][0] = box[2][0] - math.cos(a1) *10
                    box[2][1] = box[2][1] + math.sin(a1) *10
                    box[1][0] = box[1][0] - math.cos(a1) *10
                    box[1][1] = box[1][1] + math.sin(a1) *10

            if keyboard.is_pressed('down'):
                if(box[1][0] > box[3][0]):   
                    a1 = math.atan2(box[0][1]-box[3][1], box[0][0]-box[3][0])
                    a2 = math.atan2(box[1][1]-box[2][1], box[1][0]-box[2][0])
                    box[2][0] = box[2][0] - math.cos(a2) *10
                    box[2][1] = box[2][1] - math.sin(a2) *10
                    box[3][0] = box[3][0] - math.cos(a1) *10
                    box[3][1] = box[3][1] - math.sin(a1) *10
                else: 
                    a1 = math.atan2(box[0][1]-box[1][1], box[0][0]-box[1][0])
                    box[0][0] = box[0][0] - math.cos(a1) *10
                    box[0][1] = box[0][1] + math.sin(a1) *10
                    box[3][0] = box[3][0] - math.cos(a1) *10
                    box[3][1] = box[3][1] + math.sin(a1) *10

            if keyboard.is_pressed('left'):
                if(box[1][0] > box[3][0]):   
                    a1 = math.atan2(box[0][1]-box[1][1], box[0][0]-box[1][0])
                    box[0][0] = box[0][0] + math.cos(-a1) *10
                    box[0][1] = box[0][1] - math.sin(-a1) *10
                    box[3][0] = box[3][0] + math.cos(-a1) *10
                    box[3][1] = box[3][1] - math.sin(-a1) *10
                else: 
                    a1 = math.atan2(box[0][1]-box[3][1], box[0][0]-box[3][0])
                    a2 = math.atan2(box[1][1]-box[2][1], box[1][0]-box[2][0])
                    box[0][0] = box[0][0] + math.cos(a1) *10
                    box[0][1] = box[0][1] + math.sin(a1) *10
                    box[1][0] = box[1][0] + math.cos(a2) *10
                    box[1][1] = box[1][1] + math.sin(a2) *10

            if keyboard.is_pressed('right'):
                if(box[1][0] < box[3][0]):
                    a1 = math.atan2(box[2][1]-box[1][1], box[2][0]-box[1][0]) 
                    box[2][0] = box[2][0] + math.cos(-a1) *10
                    box[2][1] = box[2][1] - math.sin(-a1) *10
                    box[3][0] = box[3][0] + math.cos(-a1) *10
                    box[3][1] = box[3][1] - math.sin(-a1) *10
                else:
                    a1 = math.atan2(box[1][1]-box[0][1], box[1][0]-box[0][0]) 
                    box[1][0] = box[1][0] + math.cos(-a1) *10
                    box[1][1] = box[1][1] - math.sin(-a1) *10
                    box[2][0] = box[2][0] + math.cos(-a1) *10
                    box[2][1] = box[2][1] - math.sin(-a1) *10

            newRec = border.copy()
            cv2.drawContours(newRec,[box],0,(0,0,0),3)
            #cv2.rectangle(newRec,(x+bordersize,y+bordersize),(x+bordersize+w,y+bordersize+h),(0,0,0),3)
            cv2.imshow('movedRec',  newRec) 
            cv2.waitKey()
            #cv2.destroyAllWindows()
    if keyboard.is_pressed('g'):  # if key 'q' is pressed 
            accept = True
    else:
        accept = False
    cord = (int(90 + x + w*.5), int(180 + y + h*.5))
    cv2.destroyAllWindows()
    if regRec:
        return [w, h], accept, cord
    elif box[1][0] < box[3][0]:
        #(p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        return [np.linalg.norm(box[0] - box[3]), np.linalg.norm(box[0] - box[1])], accept, (int((box[0][0]-10+box[2][0]-10) / 2),int((box[0][1]+box[2][1]+160) / 2))
    else:
        return [np.linalg.norm(box[2] - box[3]), np.linalg.norm(box[2] - box[1])], accept, (int((box[0][0]-10+box[2][0]-10) / 2), int((box[0][1]+box[2][1]+160) / 2))
   


def main():

    #dataframe to hold cow width,length,breed,height

    df = pd.DataFrame(columns=['width','length','height','breed', 'weight', 'accepted','fileLoc'],dtype = object)
    
    #folder to read from
    inputFolder = r"C:\Users\indes\PycharmProjects\VT_Animal_SCI_ISE\RealsenseCameraTriggers\FarmVisit7\FarmVisit7"
    
    #loops through all folders
    for filename in os.listdir(inputFolder):
        #loops throguh images
        print(filename)
        for picture in os.listdir(inputFolder  + '\\' + filename):
            print(filename)
            if(('.png' in picture) & ('Color' not in picture)):
                #Width, Length, accepted
                cowValues, accept, heightCord = getCowDim(cv2.imread(inputFolder  + '\\' +  filename +'\\'  +  picture))
                print(filename.split('.bag')[0] + '.bag')
                #Heightvs
                pictureName = picture.split('.bag')[0] + '.bag'
                height = getHeight("".join([inputFolder,'\\', filename, '\\',pictureName]), heightCord[0], heightCord[1])
                #Breed
                if ('T' in filename):
                    breed = 'Jersey'
                else:
                    breed = 'Holstein'
                #Append to dataFrame
                df.loc[len(df)] = [cowValues[0], cowValues[1], height, breed, int(filename[:-1]), accept, filename +'\\'  +  picture]
                print(df)
        df.to_csv('Sample_text22.csv')

# Hear instead of saving the model you can import Cow weight estimation from cow_identifier.py and use the data from their instead of making a full dataset


#counters used for threshold result naming
#set cowsPerSet to number of pictures in each set

    
if __name__ == "__main__":
    main()
