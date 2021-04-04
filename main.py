import pyautogui,sys
from classes import imageClass
from classes import garticClass
from PIL import Image
from pynput.mouse import Listener

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

colorPositions = (
    (346, 409)
    , (391, 407)
    , (436, 406)
    , (344, 455)
    , (346, 409)
    , (391, 407)
    , (436, 406)
    , (344, 455)
    , (346, 409)
    , (391, 407)
    , (436, 406)
    , (344, 455)
    , (346, 409)
    , (391, 407)
    , (436, 406)
    , (344, 455)
    , (346, 409)
    , (391, 407)
)

firstClick =(0,0)
secondClick = (0,0)


def drawPoint(numColor, position):
    pyautogui.click(x=colorPositions[numColor][0], y=colorPositions[numColor][1])
    pyautogui.click(x=position[0], y=position[1])


def on_click(x, y, button, pressed):
    global clickNumber, firstClick, secondClick
    if clickNumber == 2:
        clickListener.stop()
    if pressed and clickNumber == 1:
        clickNumber+=1
        firstClick = (x,y)
        print('Deuxième clic ({0}, {1}) with {2}'.format(x, y, button))
    if pressed and clickNumber == 0:
        clickNumber+=1
        secondClick = (x,y)
        print('Premier clic ({0}, {1}) with {2}'.format(x, y, button))

with Listener(on_click=on_click) as clickListener:
    clickListener.join()

resizedWidth = abs(secondClick[0]-firstClick[0])
resizedHeight = abs(secondClick[1]-firstClick[1])


originalImage = Image.open("imgs/cat.jpg")
imageToDraw = originalImage.resize((resizedWidth, resizedHeight))


imgWidth = imageToDraw.width  # Get the width and hight of the image for iterating over
imgHeight = imageToDraw.height  # Get the width and hight of the image for iterating over

imgFinal = {}



for x in range(imgWidth):
    for y in range(imgHeight):
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
       
print(imgFinal)

for x in range(imgWidth):
    for y in range(imgHeight):
        print(imgFinal[(x,y)])



    