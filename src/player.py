from pyautogui import press, keyDown, keyUp
from imageProcess import ImageProcess
from screencapture import ScreenCapture
from time import sleep
import sys, os
import random

class Player:

    def __init__(self):
        self.score = None
        self.decisionGenes = {'double_cactus_small': None,
                                'quadruple_cactus': None,
                                'single_cactus': None,
                                'single_small_cactus': None,
                                'triple_cactus': None}

        for key in self.decisionGenes.keys():
            self.decisionGenes[key] = [ [ [] for i in range(100) ] for i in range(951) ]

        self.create_genetic_info()

    def jump(self, time = 0.1): #press up key for `time` seconds
        press('up', _pause= time)

    def duck(self, time = 0.1): #press the down key for `time` seconds
        press('down', _pause= time)

    def create_genetic_info(self):

        for key in self.decisionGenes.keys():
            for i in range(len(self.decisionGenes[key])):
                for j in range( len(self.decisionGenes[key][i]) ):

                    coinFlip = random.randint(0,100)

                    if coinFlip % 2 == 0:
                        self.decisionGenes[key][i][j] = self.duck
                    else:
                        self.decisionGenes[key][i][j] = self.jump





    def play(self):

        #create Imageprocess object to see what is happening in the game
        template_files = os.listdir('images/obstacle_images')
        for index, fileName in enumerate(template_files):
            template_files[index] = 'images/obstacle_images/' + fileName
        dinosaur_image_path = r'images/dinosaur.PNG'
        game_vision = ImageProcess(template_files, dinosaur_image_path) #get vision of the game

        game_over = False
        ScreenCapture.get_screen(delay = 5) #delay to put game into focus
        press('space') #start game


        while not game_over:
            #game starts. find image and make play
            img = ScreenCapture.get_screen(top = 300, left = 1000, width = 700, height = 200, delay = 0)
            res = game_vision.get_distance(img)
            if res != -1:
                for obstacle, distance in res.items():

                    # the action is that obstacle's action is the gene
                    #encoded for the obstacle and its x, y distance
                    action = self.decisionGenes[obstacle][distance[0]][distance[1]]
                    action()

            else:
                game_over = True


def main():
    player = Player()
    player.play()

if __name__ == "__main__":
    main()