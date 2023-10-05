#-----------------------------------------------
# This is small program to convert any video to 
# ascii.
#
# It use webcam 
# TODO:
# 1. Stablization 
# 2. Option to choose which to vid feed
#-----------------------------------------------




import cv2 as cv
import os
import copy
import pygame as pg
from multiprocessing import Process

video = ['bad_apple.mp4', 'hill.webm', 'b.webm', 'z.mp4', 'o.mp4']
audio =['bad_apple.mp3']

# pg.init()
# song = pg.mixer.music.load(audio[0])
# pg.mixer.music.play()

vid = cv.VideoCapture(video[2])
# vid = cv.VideoCapture(0)

img_width = 0
img_height = 0

def nothing(x):
    pass

def toAscii(img):

    #NOTE:
    #----------------------------------------
    # This function convert to ascii 
    # The width_div and height_div are the divisor
    # for ascii screen size, the default size is
    # given. You may tune with the value to fit 
    # need.
    #----------------------------------------

    symbols = ['*','-',',','#','+','^','!','.']
    # symbols = ["$", "#" ,"S" ,"%" ,"?" ,"*" ,"+" , ";", ":", "," "."]
    size = len(symbols)

    w, h = img.shape
    if w <=500:
        width_div = w//96
    else:
        width_div = w//144 
        # width_div = w//135 

    height_div = h//35   

        #NOTE:
        # The image width and height should need to choose 
        # The default width is img_width//144 and height is img_height//35
        # In some case the width is different 
        # The actual size it difficult to calculate, you need to tune it yourself

    img = cv.resize(img, (w//width_div, h//height_div))

    output = " "
    for row in img:
        for i in row:
            output += symbols[i % size]
        output+='>'

    last = 0
    for index, _ in enumerate(copy.copy(output)):
        if output[index] == '>':
            print( output[last:index + 1] )
            last = index + 1

def play():

    cv.namedWindow("track")
    cv.createTrackbar('threshold','track',0,255,nothing)

    while True:
        ret, ori = vid.read()
        # img = cv.flip(img, 1)


        if not ret:
            print('camera not found')
            exit(1)
        
        img = cv.cvtColor(ori, cv.COLOR_BGR2GRAY)
        threshold = cv.getTrackbarPos('threshold','track')
        # threshold = 128 
        img = cv.threshold(img, threshold, 255, cv.THRESH_BINARY_INV)[1]

        

        #NOTE:
        # The image width and height should need to choose 
        # The default width is img_width//144 and height is img_height//35
        # In some case the width is different 
        # The actual size it difficult to calculate, you need to tune it yourself

        p = Process(target=toAscii,
                    args=(img,),)
        p.start()
        p.join()

        # print(img.shape)
        
        cv.imshow('frame', img)
        # cv.imshow('ori', ori)
        cv.imshow('track', threshold)

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=='__main__':
    play()
    vid.release()
    cv.destroyAllWindows()
