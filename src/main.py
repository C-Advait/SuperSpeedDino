from screencapture import ScreenCapture
from imageProcess import ImageProcess
import sys, os
import cv2
import numpy
import time
from mss.windows import MSS as mss
from pynput.mouse import Button, Controller
from player import Player

sys.path.append("/../")


def play_game():
    player = Player()
    print('5s to get screen open')
    time.sleep(5)
    player.play()



def main():

    # load obstacles
    template_files = os.listdir("images/obstacle_images")
    for index, fileName in enumerate(template_files):
        template_files[index] = "images/obstacle_images/" + fileName

    # Create image processing object to use detection with
    imgProcess = ImageProcess(template_files, "images/dinosaur.PNG")

    #get image and find distance to all obstacles
    img = ScreenCapture.get_screen(
        top = 160, left = 980, width = 600,
        height = 130, delay = 0
        )
    res = imgProcess.get_distance(img, drawRect = True)
    print(res)
    #get score of the run
    score_img = ScreenCapture.get_screen(
        top=135, left=1500, width=90, height=30, delay=0
    )
    # imgProcess.show_image(cv2.cvtColor(score_img, cv2.COLOR_BGRA2GRAY))
    score = imgProcess.get_score(score_img)
    print(int(score))


if __name__ == "__main__":
    # play_game()
    main()