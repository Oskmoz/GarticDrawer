import sys
from classes import imageClass
from classes import garticClass
from PIL import Image
from pynput.mouse import Listener

clickNumber = 0
garticColors = garticClass.Gartic()

print(garticColors.getColors())


def on_click(x, y, button, pressed):
    global clickNumber
    if clickNumber == 2:
        clickListener.stop()
    if pressed:
        clickNumber+=1
        print('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

with Listener(on_click=on_click) as clickListener:
    clickListener.join()

imageToDraw = Image.open("imgs/cat.jpg")

imgWidth = imageToDraw.width  # Get the width and hight of the image for iterating over
imgHeight = imageToDraw.height  # Get the width and hight of the image for iterating over

for x in range(imgWidth):
    for y in range(imgHeight):
        print(imageToDraw.getpixel((x,y)))