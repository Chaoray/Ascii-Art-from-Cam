from PIL import Image
import cv2
import numpy as np
import win32console, win32con
import math

compressionRate = 10  # 1000%
AsciiChars = [ "#", "#", "@", "%", "=", "+", "*", ":", "-", ".", " " ]
AsciiCharsLength = len(AsciiChars) - 1

# where magic started
sizeSet = True
consoleBufferHandle = win32console.CreateConsoleScreenBuffer(DesiredAccess = win32con.GENERIC_READ | win32con.GENERIC_WRITE, ShareMode=0, SecurityAttributes=None, Flags=1) # create console buffer
consoleBufferHandle.SetConsoleActiveScreenBuffer() # set this handle to console buffer

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Unable to catch camera, make sure you inserted it")
    exit()

while(True):
    success, frame = cap.read()
    if not success:
        print("Unable to receive frame. Exiting ...")
        break

    cv2.imshow('live', frame)  # uncomment it if you wanna compare the original frame

    pimg = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    buffer = ''
    for y in np.arange(0, pimg.height, compressionRate):
        for x in np.arange(0, pimg.width, compressionRate):
           index = int((pimg.getpixel((x, y)) * AsciiCharsLength) / 255)
           buffer += AsciiChars[index]
        buffer += '\n'
    
    if not sizeSet:
        try:
            width = math.ceil(pimg.width / compressionRate) + 1
            height = math.ceil(pimg.height / compressionRate) + 1
            size = win32console.PyCOORDType(width, height)
            consoleBufferHandle.SetConsoleScreenBufferSize(size)
            sizeSet = True
        except:
            pass

    consoleBufferHandle.WriteConsole(buffer) # write output to console buffer
    # and if you don't understand the code I wrote, that's ok, it's not a common to print things, but it really plays an important part in windows

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('w'):
        compressionRate += 0.1
        sizeSet = False
    elif key == ord('s'):
        compressionRate -= 0.1
        sizeSet = False
    

cap.release()
cv2.destroyAllWindows()