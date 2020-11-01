
import os, sys, time
sys.path.append('./src/')
from imageProcess import ImageProcess
from screencapture import ScreenCapture

def main():

    # load obstacles
    template_files = os.listdir(r"test/image_recog/obstacles")
    for index, fileName in enumerate(template_files):
        template_files[index] = r'test/image_recog/obstacles/' + fileName

    dinosaur_path = 'images/dinosaur.PNG'

    # Create image processing object to use detection with
    imgProcess = ImageProcess(template_files, dinosaur_path)

    print('focus game')
    time.sleep(3)
    i = 0
    gameOver = False
    while gameOver != -1:
        img = ScreenCapture.get_screen(
            top = 300, left = 1000, width = 700,
            height = 200, delay = 0
            )
        gameOver = imgProcess.createVideo(img, fileName= str(i))
        i += 1

if __name__ == "__main__":
    main()

