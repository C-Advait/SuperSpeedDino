from screencapture import ScreenCapture
from imageProcess import ImageProcess
import sys, os
import cv2
import numpy
from time import time
from mss.windows import MSS as mss
from pynput.mouse import Button, Controller
from time import time


sys.path.append('/../')

def main():

    #load obstacles
    template_files = os.listdir('images/obstacle_images')
    for index, fileName in enumerate(template_files):
        template_files[index] = 'images/obstacle_images/' + fileName

    #Create image processing object to use detection with
    imgProcess = ImageProcess(template_files, 'images/dinosaur.PNG')

    #get image and find distance to all obstacles
    img = ScreenCapture.get_screen(top = 300, left = 1000, width = 700, height = 200)
    res = imgProcess.get_distance(img, drawRect = True)
    print(res)

    # #get score of the run
    # score_img = ScreenCapture.get_screen(top = 300, left = 1080, width = 200, height = 50)
    # imgProcess.show_image(cv2.cvtColor(score_img, cv2.COLOR_BGRA2GRAY))
    # imgProcess.get_score(score_img)


if __name__ == "__main__":
    main()