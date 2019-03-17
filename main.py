import maestro as m
import time
import cv2 
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera




def __main__():
        x = m.Controller()
        camera(x)
        #drive(x)




def camera(x):
    x.setTarget(1,6000)
    x.setTarget(2,6000)
    # initialize the camera and grab a reference to the raw camera capture
    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 32
    rawCapture = PiRGBArray(camera, size=(640, 480))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(9,9))

    # allow the camera to warmup
    time.sleep(0.1)

    # capture frames from the camera
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
        image = frame.array
        height,width,channles = image.shape
        image = image[400:480, 0:640]
        blur = cv2.blur(image,(7,7))
        #image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)    
        #lower = np.array([180,0,90])
        #upper = np.array([245,30,160])
        #mask = cv2.inRange(image,lower,upper)
        #result = cv2.bitwise_and(image,image,mask=mask)
        pic = cv2.Canny(blur, 100, 170)
        final = cv2.dilate(pic,kernel,iterations=2)
        r, thresh = cv2.threshold(final, 20, 255, cv2.THRESH_BINARY)
        conts, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        bestCon = None
        bestY = -1
		
        for c in conts:
            (coordX,y),radius = cv2.minEnclosingCircle(c)
            coordX = int(coordX)
            y= int(y)
            #if(y > bestY):
            if(y > bestY):
                bestY = y
                bestCon = c
				
        if(bestCon != None):	
            (coordX,y),radius = cv2.minEnclosingCircle(bestCon)
            height, width = final.shape
            middle = int(width/2)
            print("middle = " + str(middle) + "coordX = " + str(coordX))
            if(middle -30 < coordX < middle + 30):
                move(x)
                print("not turning")
            elif(coordX > middle+30):
                print("turn right")
                moveRight(x)
                #move(x)
            else:
                print("turn left")
                moveLeft(x)
                #move(x)
			
		
        # show the frame
        cv2.imshow("Frame", final)
        if cv2.countNonZero(final)==0:
            print("black")
            x.setTarget(1,6000)
            x.setTarget(2,6000)
            exit()
        else:
            #x.setTarget(1,x.getPosition(1)-50)
            move(x)
            print("gooo") 

        key = cv2.waitKey(1) & 0xFF
        # clear the stream in preparation for the next frame
        rawCapture.truncate(0)
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break
                              

def moveRight(x):
    x.setTarget(2,x.getPosition(2)-1000)
    time.sleep(.15)
    reset(x)

def moveLeft(x):
    x.setTarget(2,x.getPosition(2)+1000)
    time.sleep(.15)
    reset(x)
	
def move(x):
    x.setTarget(1,x.getPosition(1)-600)
    time.sleep(.15)
    reset(x)

def reset(x):
    x.setTarget(1,6000)
    x.setTarget(2,6000)	
							  
def drive(x):

    x.setTarget(1,6000)
    x.setTarget(2,6000)
    stop = False
    while(not stop):
        cmd = input("input:\n")

        #Go reverse, increments by 650 everytime w is pressed
        if(cmd=='s'):
            if x.getPosition(1)<8000:
                x.setTarget(1, x.getPosition(1)+650)

        #go in forward
        elif(cmd=='w'):
            if x.getPosition(1)>4000:
                x.setTarget(1, x.getPosition(1)-650)

        #2 stops the movement of the wheels
        elif(cmd=='2'):
            x.setTarget(1,6000)
            x.setTarget(2,6000)
        
        elif cmd=='a':
            if x.getPosition(2)<7400:
                x.setTarget(2, x.getPosition(2)+700)
        #turn right
        elif cmd=='d':
            if x.getPosition(2)>4600:
                 x.setTarget(2, x.getPosition(2)-700)


        #########################Head Movement####################
        #turn head up
        elif cmd=='t':
            if x.getPosition(4)<8000:
                x.setTarget(4, x.getPosition(4)+1000)
        #turn head down
        elif cmd=='g':
            if x.getPosition(4)>4000:
                x.setTarget(4, x.getPosition(4)-1000)
                                                                                
        #turn head left
        elif cmd=='f':
            if x.getPosition(3)<8000:
                x.setTarget(3, x.getPosition(3)+1000)
        #turn head right
        elif cmd=='h':
            if x.getPosition(3)>4000:
                x.setTarget(3, x.getPosition(3)-1000)                                                                               

        #quit program
        elif(cmd=='p'):
            stop = True

__main__()

