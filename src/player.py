from pyautogui import press, keyDown, keyUp
from imageProcess import ImageProcess
from screencapture import ScreenCapture
from time import sleep
import cv2
import time
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
            self.decisionGenes[key] = [[[] for i in range(100)] for i in range(600)]

        self.create_genetic_info()

    def jump(self, time, keypressMut):  # press up key for `time` seconds
        if keypressMut.acquire(blocking=False):
            # print("action is jump, time = ", time)
            keyDown("up")
            keyup_timer = threading.Timer(time, keyUp, args = ("up", ) )
            lock_release_timer = threading.Timer(time, keypressMut.release)
            keyup_timer.start()
            lock_release_timer.start()
        else:
            # print('another action has not released')
            pass

    def duck(self, time, keypressMut):  # press the down key for `time` seconds

        if keypressMut.acquire(blocking= False):
            # print('action is duck, time = ', time)
            keyDown("down")
            keyup_timer = threading.Timer(time, keyUp, args = ("down", ))
            lock_release_timer = threading.Timer(time, keypressMut.release)
            keyup_timer.start()
            lock_release_timer.start()
        else:
            # print('another action has not released')
            pass

    def do_nothing(self, time, keypressMut):

        if keypressMut.acquire(blocking=False):
            # print('action is nothing, time = ', time)
            lock_release_timer = threading.Timer(time, keypressMut.release)
            lock_release_timer.start()
        else:
            # print('another action has not released')
            pass


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

        keypressMut = threading.Lock()
        # create Imageprocess object to see what is happening in the game
        template_files = os.listdir("images/obstacle_images")
        for index, fileName in enumerate(template_files):
            template_files[index] = "images/obstacle_images/" + fileName
        dinosaur_image_path = r"images/dinosaur.PNG"
        game_vision = ImageProcess(
            template_files, dinosaur_image_path
        )  # get vision of the game

        game_over = False
        time.sleep(1) #game actually resets
        press("space")  # start game
        time.sleep(1) #game starts
        print("game started ")
        if keypressMut.locked():
            print('mutex acquired at start of individual')

        while not game_over:
            # game starts. find image and take action
            img = ScreenCapture.get_screen(
                top = 160, left = 340, width = 600, height = 150, delay = 0
            )
            res = game_vision.get_distance(img)
            if res != -1:
                for obstacle, distance in res.items():

                    # the action is that obstacle's action is the gene
                    # encoded for the obstacle and its x, y distance
                    action, sleep = self.decisionGenes[obstacle][distance[0]][
                        distance[1]
                    ]
                    # print("res = ", res, 'action is: ', action, 'sleep = ', sleep)
                    action(sleep, keypressMut)

            else:
                game_over = True
        score_img = ScreenCapture.get_screen(
           top=120, left=860, width=100, height = 50, delay=2,
        )
        score_img = cv2.cvtColor(score_img, cv2.COLOR_BGRA2GRAY)
        score = int(game_vision.get_score(score_img))
        # print('game done', score, '\n')

        return score

    def __len__(self):
        return 95100


def main():
    player = Player()
    sleep(2)
    player.play()


if __name__ == "__main__":
    main()
