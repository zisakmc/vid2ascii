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
import copy
from multiprocessing import Process
video = ['bad_apple.mp4', 'hill.webm']
audio =['bad_apple.mp3']

vid = cv.VideoCapture(video[0])
# vid = cv.VideoCapture(0)
img_width = 0
img_height = 0

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
    while True:
        ret, img= vid.read()
        # img = cv.flip(img, 1)


        if not ret:
            print('camera not found')
            exit(1)
        
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        threshold = 100 
        img = cv.threshold(img, threshold, 255, cv.THRESH_BINARY)[1]

        

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

        if cv.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=='__main__':
    play()
    vid.release()
    cv.destroyAllWindows()
