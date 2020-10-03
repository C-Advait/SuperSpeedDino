from screencapture import windowCapture
from imageProcess import imageProcess
import sys, os
import cv2
import numpy
from time import time
from mss.windows import MSS as mss
from pynput.mouse import Button, Controller
from time import time


def main():


    img = windowCapture.get_screen()
    imageProcess.show_image(img)

def loop_run():
    loop_time = time()
    while(True):
        screenshot = windowCapture.get_screen()

        # cv2.imshow('image',screenshot)
        print('FPS is {}'.format(1/ (time() - loop_time)))
        loop_time= time()

        #GAIN OF 30 FPS if not using if check
        # if cv2.waitKey(1) == ord('q'):
        #     cv2.destroyAllWindows()
        #     break

if __name__ == "__main__":
    main()