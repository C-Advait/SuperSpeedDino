from screencapture import ScreenCapture
from imageProcess import ImageProcess
import sys, os, cv2, time
import numpy as np
from player import Player1D, Player2D
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
            top = 170, left = 378, width = 600,
            height = 120, delay = 0
        )

    cv2.imshow('test', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    res = imgProcess.get_distance(img, drawRect = True)
    print(res)
    # raise IndexError
    #get score of the run
    score_img = ScreenCapture.get_screen(
        top=140, left= 914, width=60, height=25, delay=0
    )
    # imgProcess.show_image(cv2.cvtColor(score_img, cv2.COLOR_BGRA2GRAY))
    score = imgProcess.get_score(score_img, show_score=True)
    print(int(score))

    img2 = ScreenCapture.get_screen(
            top = 172, left = -1524, width = 400,
            height = 120, delay = 0
        )
    imgProcess.createVideo(img2, 'testing.bmp')


if __name__ == "__main__":
    # play_game()
    main()
    # cursorpos()