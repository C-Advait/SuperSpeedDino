from screencapture import windowCapture
import sys, os
import cv2
import numpy
from time import time
from mss.windows import MSS as mss 
from pynput.mouse import Button, Controller
from time import time

def main():

    with mss() as sct:
        monitor = {"top": 40, "left": 0, "width": 800, "height": 640}
        while "Screen capturing":
            last_time = time()

            # Get raw pixels from the screen, save it to a Numpy array
            img = numpy.array(sct.grab(monitor))

            # Display the picture
            # cv2.imshow("OpenCV/Numpy normal", img)

            # Display the picture in grayscale
            cv2.imshow('OpenCV/Numpy grayscale', 
                       cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

            print("fps: {}".format(1 / (time() - last_time)))

            # Press "q" to quit
            if (cv2.waitKey(1) & 0xFF == ord("q")):
                cv2.destroyAllWindows()
                break


    """
    windowCapture.list_windows_names()    
    loop_time = time()
    input("Press Enter to continue...")
    screenshot = windowCapture.get_screen()

    cv2.imshow('image',screenshot)
    loop_time= time()
    

    cv2.waitKey(0)
    # loop_run()
    """
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