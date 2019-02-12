# -*- coding: utf-8 -*-
"""
Created on Fri Feb  8 14:59:29 2019

@author: tuguluth
"""

'''
 * Python program to use contours to extract the dice in an image, to then add up totals.
'''
import cv2   #Key module allows me to check the number of dice
import sys   # Filepaths
import os    # Pip detection
import numpy as np

# read command-line arguments
#filename = sys.argv[1]
#t = int(sys.argv[2])

#Delete privious files if exist
for filenames in os.listdir("S:\Business Solutions\ThomasT\Current\Armoury\Macros\Dice"):
    if "sub" in filenames:
        os.remove(filenames)

#Use Masking of white areas to find the dice.

def getSobel (channel):

    sobelx = cv2.Sobel(channel, cv2.CV_16S, 1, 0, borderType=cv2.BORDER_REPLICATE)
    sobely = cv2.Sobel(channel, cv2.CV_16S, 0, 1, borderType=cv2.BORDER_REPLICATE)
    sobel = np.hypot(sobelx, sobely)

    return sobel;

def findSignificantContours (img, sobel_8u):
    contours, heirarchy = cv2.findContours(sobel_8u, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find level 1 contours
    level1 = []
    for i, tupl in enumerate(heirarchy[0]):
        # Each array is in format (Next, Prev, First child, Parent)
        # Filter the ones without parent
        if tupl[3] == -1:
            tupl = np.insert(tupl, 0, [i])
            level1.append(tupl)

    # From among them, find the contours with large surface area.
    significant = []
    tooSmall = sobel_8u.size * 5 / 100 # If contour isn't covering 5% of total area of image then it probably is too small
    for tupl in level1:
        contour = contours[tupl[0]];
        area = cv2.contourArea(contour)
        if area > tooSmall:
            cv2.drawContours(img, [contour], 0, (0,255,0),2, cv2.LINE_AA, maxLevel=1)
            significant.append([contour, area])

    significant.sort(key=lambda x: x[1])
    return [x[0] for x in significant];

def segment (path):
    img = cv2.imread(path)

    blurred = cv2.GaussianBlur(img, (5, 5), 0) # Remove noise

    # Edge operator
    sobel = np.max( np.array([ getSobel(blurred[:,:, 0]), getSobel(blurred[:,:, 1]), getSobel(blurred[:,:, 2]) ]), axis=0 )

    # Noise reduction trick, from http://sourceforge.net/p/octave/image/ci/default/tree/inst/edge.m#l182
    mean = np.mean(sobel)

    # Zero any values less than mean. This reduces a lot of noise.
    sobel[sobel <= mean] = 0;
    sobel[sobel > 255] = 255;

    cv2.imwrite('output/edge' + path + '.png', sobel);

    sobel_8u = np.asarray(sobel, np.uint8)

    # Find contours
    significant = findSignificantContours(img, sobel_8u)

    # Mask
    mask = sobel.copy()
    mask[mask > 0] = 0
    cv2.fillPoly(mask, significant, 255)
    # Invert mask
    mask = np.logical_not(mask)

    #Finally remove the background
    img[mask] = 0;

    fname = path.split('/')[-1]
    cv2.imwrite('output/' + fname, img);
    print (path)


segment('Dice18.jpg')



# =============================================================================
# contours, hierachy = cv2.findContours(, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# # use the contours to extract each image, into a new sub-image
# for (i, c) in enumerate(contours):
#     (x, y, w, h) = cv2.boundingRect(c)
#     # use slicing and the (x, y, w, h) values of the bounding
#     # box to create a subimage based on this contour
#     if x + w >= 25:
#         subImg = img[y : y + h, x : x + w, :]
#     
#         # save the subimage as sub-x.jpg, where x is the number
#         # of this contour.
#         cv2.imwrite("sub-{}.jpg".format(i), subImg)
# cv2.imwrite("Imgcheck.jpg".format(i), fgmask)   
#  
# 
# #Set Dice Count
# Ones = 0
# Twos = 0
# Threes = 0
# Fours = 0
# Fives = 0
# Sixes = 0
# UnknownDie = 0
# z = 0
# # Now we're looking to do pip detection on each image
#     
# # read original image
# 
# for filenames in os.listdir("S:\Business Solutions\ThomasT\Current\Armoury\Macros\Dice"):
#     if "sub" in filenames:
#         filename = filenames
#         
#         img = cv2.imread(filename)
#         [y, x] = np.shape(img[:,:,0])
# 
#         if y >= 25:
#             z = z+1
#             # create binary image
#             gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#             blur = cv2.GaussianBlur(gray, (5, 5), 0)
#             (t, binary) = cv2.threshold(blur, t, 255, cv2.THRESH_BINARY)
#             
#             # find contours
#             (contours, hierarchy) = cv2.findContours(binary, cv2.RETR_TREE, 
#             cv2.CHAIN_APPROX_SIMPLE)
#             
#             # Count the number of pips on the dice faces.
#             # Iterate through hierarchy[0], first to find the indices of dice
#             # contours, then again to find pip contours.
#             
#             dice = []   # list of dice contours
#             pips = []   # list of pip contours
#             
#             # find dice contours
#             for (i, c) in enumerate(hierarchy[0]):
#                 if c[3] == -1:
#                     dice.append(i)
#                     
#             # find pip contours
#             for (i, c) in enumerate(hierarchy[0]):
#                 if c[3] in dice:
#                     pips.append(i)
#                         
#     
#             if len(pips) == 1:
#                 Ones = Ones + 1
#             elif len(pips) == 2:
#                 Twos = Twos + 1
#             elif len(pips) == 3:
#                 Threes = Threes + 1
#             elif len(pips) == 4:
#                 Fours = Fours + 1    
#             elif len(pips) == 5:
#                 Fives = Fives + 1
#             elif len(pips) == 6:
#                 Sixes = Sixes + 1
#             else:
#                 UnknownDie = UnknownDie + 1
#                 z = z-1
# 
# print("Total Ones:", Ones)    
# print("Total Twos:", Twos)              
# print("Total Threes:", Threes)              
# print("Total Fours:", Fours)              
# print("Total Fives:", Fives)              
# print("Total Sixes:", Sixes)              
# print("Total Unknown Shapes:", UnknownDie)
# print("Dice Rolled:", z)    
# =============================================================================
