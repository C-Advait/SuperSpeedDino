from pyautogui import press, keyDown, keyUp
from imageProcess import ImageProcess
from screencapture import ScreenCapture
from time import sleep
import sys, os
import random
import threading


class Player:

    decisionGenes = {
        "double_cactus_small": None,
        "quadruple_cactus": None,
        "single_cactus": None,
        "single_small_cactus": None,
        "triple_cactus": None,
    }

    def __init__(self):
        self.score = None

        for key in self.decisionGenes.keys():
            self.decisionGenes[key] = [[[] for i in range(100)] for i in range(951)]

        self.create_genetic_info()

    def raise_wait(self, time):
        pass

    def jump(self, time=1):  # press up key for `time` seconds
        keyDown("up")
        sleep(time)
        keyUp("up")

    def duck(self, time=1):  # press the down key for `time` seconds
        keyDown("down")
        sleep(time)
        keyUp("down")

    def do_nothing(self, time=1):
        sleep(time)

    def create_genetic_info(self):

        for key in self.decisionGenes.keys():
            for i in range(len(self.decisionGenes[key])):
                for j in range(len(self.decisionGenes[key][i])):

                    randAction = random.randint(0, 2)
                    randSleep = random.uniform(0.1, 1.5)

                    if randAction == 0:
                        self.decisionGenes[key][i][j] = [self.duck, randSleep]
                    elif randAction == 1:
                        self.decisionGenes[key][i][j] = [self.jump, randSleep]
                    else:
                        self.decisionGenes[key][i][j] = [self.do_nothing, randSleep]

    def play(self):

        # create Imageprocess object to see what is happening in the game
        template_files = os.listdir("images/obstacle_images")
        for index, fileName in enumerate(template_files):
            template_files[index] = "images/obstacle_images/" + fileName
        dinosaur_image_path = r"images/dinosaur.PNG"
        game_vision = ImageProcess(
            template_files, dinosaur_image_path
        )  # get vision of the game

        game_over = False
        press("space")  # start game
        print("game started ")

        while not game_over:
            # game starts. find image and make play
            img = ScreenCapture.get_screen(
                top=300, left=1000, width=700, height=200, delay=0
            )
            res = game_vision.get_distance(img)
            if res != -1:
                for obstacle, distance in res.items():

                    # the action is that obstacle's action is the gene
                    # encoded for the obstacle and its x, y distance
                    action, sleep = self.decisionGenes[obstacle][distance[0]][
                        distance[1]
                    ]
                    print('action is: ', action, 'sleep = ', sleep)
                    action(time=sleep)

            else:
                game_over = True
        score_img = ScreenCapture.get_screen(
            top=300, left=1500, width=100, height=50, delay=0
        )
        score = int(game_vision.get_score(score_img))
        print(score)

        return score

    def __len__(self):
        return 95100


def main():
    player = Player()
    sleep(2)
    player.play()


if __name__ == "__main__":
    main()
