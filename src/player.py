from pyautogui import press, keyDown, keyUp
from imageProcess import ImageProcess
from screencapture import ScreenCapture
from time import sleep

class Player:

    def __init__(self):
        self.score = None

    def jump(self, time = 0.1): #press up key for `time` seconds
        press('up', _pause= time)

    def duck(self, time = 0.1): #press the down key for `time` seconds
        press('down', _pause= time)


    def play(self):

        #create Imageprocess object to see what is happening in the game
        obstacle_files = os.listdir('images/obstacle_images')
        for fileName in obstacle_files:
            obstacle_images += 'images/obstacle_images/' + fileName
        dinosaur_image_path = r'images\dinosaur.PNG'
        game_vision = ImageProcess(obstacle_images, dinosaur_image_path) #get vision of the game

        game_over = False
        ScreenCapture.get_screen(delay = 10) #delay to put game into focus
        press('down') #start game


        while not game_over:
            #game starts. find image and make play
            img = ScreenCapture.get_screen(delay= 0)
            res = game_vision.get_distance(img)
