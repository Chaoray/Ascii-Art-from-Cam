from PIL import Image
import cv2
import os
import numpy as np
import win32console, win32con

compressionRate = 10  # 1000%
AsciiChars = [ "#", "#", "@", "%", "=", "+", "*", ":", "-", ".", " " ]
AsciiCharsLength = len(AsciiChars) - 1

# where magic started
consoleBufferHandle = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1) # create console buffer
consoleBufferHandle.SetConsoleActiveScreenBuffer() # set this handle to console buffer
# Actually, at first I wanna use api directly, I failed, but after searching docs, I found something really interesting

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

    buffer = ''
    for y in np.arange(0, pimg.height, 1 * compressionRate):
        for x in np.arange(0, pimg.width, 1 * compressionRate):
           index = int((pimg.getpixel((x, y)) * AsciiCharsLength) / 255)
           buffer += AsciiChars[index]
        buffer += '\n'
    
    consoleBufferHandle.WriteConsole(buffer) # write output to console buffer
    # boom! 3 lines of code make output fps increase a lot!
    # and if you don't understand the code I wrote, that's ok, it's not a common to print things, but it really plays an important part in windows

cap.release()
cv2.destroyAllWindows()