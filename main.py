import pyautogui,sys
from classes import imageClass
from classes import garticClass
from PIL import Image
from pynput.mouse import Listener, Button, Controller
from pynput.keyboard import Key, Listener as keyboardListener

exitCondition = 0
clickNumber = 0
garticColors = (
    [0, 0, 0]
    , [102, 102, 102]
    , [25, 84, 198]
    , [255, 255, 255]
    , [170, 170, 170]
    , [94, 199, 250]
    , [50, 113, 45]
    , [97, 28, 15]
    , [140, 69, 32]
    , [81, 172, 176]
    , [235, 51, 42]
    , [239, 127, 64]
    , [167, 114, 48]
    , [140, 28, 77]
    , [190, 96, 91]
    , [246, 194, 77]
    , [235, 55, 141]
    , [243, 178, 171]
)

#Windows color 1920*1080
#colorPositions = (
#    (346, 409)
#    , (391, 407)
#    , (436, 406)
#    , (344, 455)
#    , (346, 409)
#    , (391, 407)
#    , (436, 406)
#    , (344, 455)
#    , (346, 409)
#    , (391, 407)
#    , (436, 406)
#    , (344, 455)
#    , (346, 409)
#    , (391, 407)
#    , (436, 406)
#    , (344, 455)
#    , (346, 409)
#    , (391, 407)
#)

#Macbook colors
colorPositions = (
    (324, 324)
    , (358, 322)
    , (395, 322)
    , (326, 360)
    , (360, 363)
    , (397, 361)
    , (322, 402)
    , (359, 401)
    , (397, 402)
    , (325, 440)
    , (357, 444)
    , (396, 442)
    , (324, 481)
    , (361, 480)
    , (395, 477)
    , (324, 516)
    , (357, 513)
    , (397, 518)
)

firstClick = (0,0)
secondClick = (0,0)
mouse = Controller()

def drawPoint(position):
    pyautogui.click(x=position[0], y=position[1])

def pickColor(numColor):
    print('New color picked : {0} '.format(numColor))
    pyautogui.click(x=colorPositions[numColor][0], y=colorPositions[numColor][1])

def drawLine(tupleCoord):
    pyautogui.moveTo(tupleCoord[0], tupleCoord[1])
    pyautogui.dragTo(tupleCoord[0], tupleCoord[2], 0.000000001, button='left')
    
def on_click(x, y, button, pressed):
    global clickNumber, firstClick, secondClick
    if clickNumber == 2:
        clickListener.stop()
    if pressed and clickNumber == 1:
        clickNumber+=1
        secondClick = (int(x),int(y))
        print('Deuxième clic ({0}, {1}) with {2}'.format(x, y, button))
    if pressed and clickNumber == 0:
        clickNumber+=1
        firstClick = (int(x),int(y))
        print('Premier clic ({0}, {1}) with {2}'.format(x, y, button))

def on_press(key):
    if key == Key.esc:
        exitCondition = 1
        sys.exit()
   
with Listener(on_click=on_click) as clickListener:
    clickListener.join()

resizedWidth = abs(secondClick[0]-firstClick[0])
resizedHeight = abs(secondClick[1]-firstClick[1])


originalImage = Image.open("imgs/poisson.jpg")
imageToDraw = originalImage.resize((resizedWidth, resizedHeight))


imgWidth = imageToDraw.width  # Get the width and hight of the image for iterating over
imgHeight = imageToDraw.height  # Get the width and hight of the image for iterating over

imgFinal = {}



for x in range(imgWidth):
    if x%5 == 0:
        for y in range(imgHeight):
            if y%5 == 0:
                pixel = imageToDraw.getpixel((x,y))
                lowestDifference = 100
                for c in range(len(garticColors)):
                    diffRed   = abs(pixel[0]   - garticColors[c][0])
                    diffGreen = abs(pixel[1] - garticColors[c][1])
                    diffBlue  = abs(pixel[2]  - garticColors[c][2])
                    pctDiffRed   = diffRed   / 255
                    pctDiffGreen = diffGreen / 255
                    pctDiffBlue  = diffBlue  / 255
                    globalDifference = (pctDiffRed + pctDiffGreen + pctDiffBlue) / 3 * 100
                    if globalDifference < lowestDifference:
                        lowestDifference = globalDifference
                        imgFinal[x,y] = c
       

drawingMatrix = []



for c in range(len(colorPositions)):
    #pickColor(c)
    drawingMatrix.append([])
    if c != 3:    
         for x in range(imgWidth):
            initialY = 0
            finalY = 0
            newLine = 0
            if x%5 == 0:
                for y in range(imgHeight):
                    if y%5 == 0:
                        if imgFinal[x,y] == c and newLine == 1 and y == range(imgHeight):
                            if finalY - initialY > 1:
                                drawingMatrix[c].append((firstClick[0]+x, firstClick[1]+initialY, firstClick[1]+finalY))
                            #drawPoint((firstClick[0]+x, firstClick[1]+initialY))
                            #drawLine(firstClick[0]+x, firstClick[1]+finalY)
                        elif imgFinal[x,y] == c and newLine == 0:
                            newLine = 1
                            initialY = y
                            finalY = y
                        elif imgFinal[x,y] == c and newLine == 1:
                            finalY = y
                        elif imgFinal[x,y] != c and newLine == 1:
                            newLine = 0
                            if finalY - initialY > 1:
                                drawingMatrix[c].append((firstClick[0]+x, firstClick[1]+initialY, firstClick[1]+finalY))
                            #drawPoint((firstClick[0]+x, firstClick[1]+initialY))
                            #drawLine(firstClick[0]+x, firstClick[1]+finalY)
                        else:
                            finalY = y


iterator = 0
for xAxis in drawingMatrix:
    pickColor(iterator)
    iterator+=1
    for yAxis in xAxis:
        drawLine(yAxis)

mouse.release(Button.left)
pyautogui.moveTo(firstClick[0], firstClick[1])