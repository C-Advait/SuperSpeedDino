from screencapture import ScreenCapture
from imageProcess import ImageProcess
import sys, os
import cv2
import numpy
import time
from mss.windows import MSS as mss
from player import Player
import win32api
sys.path.append("/../")


def play_game():
    player = Player()
    print('5s to get screen open')
    time.sleep(5)
    player.play()


def cursorpos():
    ScreenCapture.cursorPos()

def main():

    # load obstacles
    template_files = os.listdir("images/obstacle_images")
    for index, fileName in enumerate(template_files):
        template_files[index] = "images/obstacle_images/" + fileName

    # Create image processing object to use detection with
    imgProcess = ImageProcess(template_files, "images/dinosaur.PNG")

    #get image and find distance to all obstacles
    img = ScreenCapture.get_screen(
        top = 172, left = -1543, width = 600,
        height = 125, delay = 0
        )

    res = imgProcess.get_distance(img, drawRect = False)
    print(res)
    # raise IndexError
    #get score of the run
    score_img = ScreenCapture.get_screen(
        top=142, left= -1009, width=65, height=20, delay=0
    )
    # imgProcess.show_image(cv2.cvtColor(score_img, cv2.COLOR_BGRA2GRAY))
    score = imgProcess.get_score(score_img, show_score=True)
    print(int(score))


if __name__ == "__main__":
    # play_game()
    main()
    # cursorpos()