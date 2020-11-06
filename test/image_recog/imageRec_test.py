
import os, sys, time
sys.path.append('./src/')
from imageProcess import ImageProcess
from screencapture import ScreenCapture

def main():

    # load obstacles
    template_files = os.listdir(r"images/obstacle_images")
    for index, fileName in enumerate(template_files):
        template_files[index] = r'images/obstacle_images/' + fileName

    dinosaur_path = './images/dinosaur.PNG'

    # Create image processing object to use detection with
    imgProcess = ImageProcess(template_files, dinosaur_path)

    print('focus game')
    time.sleep(2)
    i = 0
    gameOver = False
    while gameOver != -1:
        img = ScreenCapture.get_screen(
            top = 172, left = -1543, width = 600,
            height = 125, delay = 0
        )
        gameOver = imgProcess.get_distance(img)
        if gameOver:
            print(gameOver)
        i += 1

if __name__ == "__main__":
    main()

