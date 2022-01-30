from PIL import Image
import cv2
import os
import numpy as np

compressionRate = 10  # 1000%
AsciiChars = [ "#", "#", "@", "%", "=", "+", "*", ":", "-", ".", " " ]
AsciiCharsLength = len(AsciiChars) - 1

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Unable to catch camera, make sure you inserted it")
    exit()

while(True):
    success, frame = cap.read()
    if not success:
        print("Unable to receive frame. Exiting ...")
        break

    #cv2.imshow('live', cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))  # uncomment it if you wanna compare the original frame

    pimg = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    outputArr = []
    for y in np.arange(0, pimg.height, 1 * compressionRate):
        for x in np.arange(0, pimg.width, 1 * compressionRate):
           index = int((pimg.getpixel((x, y)) * AsciiCharsLength) / 255)
           outputArr.append(AsciiChars[index])
        outputArr.append('\n')
    outputArr = ''.join(outputArr)
    
    print(outputArr) # I found that use array can decrease laggy
    os.system('cls')  # so is this, decrease laggy

cap.release()
cv2.destroyAllWindows()