from screencapture import windowCapture
from imageProcess import imageProcess
import sys, os
import cv2
import numpy
from time import time
from mss.windows import MSS as mss
from pynput.mouse import Button, Controller
from time import time


sys.path.append('/../')

def main():

    template_files = os.listdir('images/obstacle_images')
    for index, fileName in enumerate(template_files):
        template_files[index] = 'images/obstacle_images/' + fileName

    imgProcess = imageProcess(template_files, 'images/dinosaur.PNG')
    # img = windowCapture.get_screen()
    # # print(img)
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows
    # imgProcess.find_dino(cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY), drawRect = True)

    # # for template in imgProcess.templates:
    # #     imgProcess.find_obstacle(cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY), template, drawRect = True)
    # imgProcess.get_distance(img)

    score_img = windowCapture.get_screen(top = 300, left = 1080, width = 200, height = 50)
    imgProcess.show_image(cv2.cvtColor(score_img, cv2.COLOR_BGRA2GRAY))
    ## test
    # img = windowCapture.get_screen()
    # imageProcess.show_image(img)

    imgProcess.get_score(score_img)


if __name__ == "__main__":
    main()