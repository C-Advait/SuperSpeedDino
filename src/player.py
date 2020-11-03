from pyautogui import press, keyDown, keyUp
from imageProcess import ImageProcess
from screencapture import ScreenCapture
from time import sleep
import time
import sys, os
import random
import threading
import cv2
sys.path.append("/../")

class Player:

    def __init__(self):
        self.score = None

        obstacle_directory = "images/obstacle_images"
        file_list = os.listdir(obstacle_directory)

        self.obs_names = list( map(
            lambda x: os.path.splitext(os.path.basename(x))[0],
            file_list
        ))

        self.obs_names.remove('game_over')

        self.decisionGenes = { name: None for name in self.obs_names}
        print(self.decisionGenes)

        for key in self.decisionGenes.keys():
            self.decisionGenes[key] = [[[] for i in range(100)] for i in range(951)]

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

        #ground obstacles can only be jumped over
        #bird can be ducked or jumped over
        ground_obs_actions = [self.jump, self.do_nothing]
        bird_obs_actions = [self.jump, self.do_nothing, self.duck]


        for key in self.decisionGenes.keys():
            if 'bird' not in key:
                for i in range(len(self.decisionGenes[key])):
                    for j in range(len(self.decisionGenes[key][i])):

                        randSleep = random.uniform(0.1, 1.5)

                        self.decisionGenes[key][i][j] = [
                            random.choice(ground_obs_actions),
                            randSleep
                        ]
            else:
                for i in range(len(self.decisionGenes[key])):
                    for j in range(len(self.decisionGenes[key][i])):

                        randSleep = random.uniform(0.1, 1.5)

                        self.decisionGenes[key][i][j] = [
                            random.choice(bird_obs_actions),
                            randSleep
                        ]

    def play(self):

        keypressMut = threading.Lock()
        # create Imageprocess object to see what is happening in the game

        dinosaur_image_path = r"images/dinosaur.PNG"
        game_vision = ImageProcess(
            self.obs_names , dinosaur_image_path
        )  # get vision of the game

        game_over = False
        time.sleep(1) #game actually resets
        press("space")  # start game
        time.sleep(1) #game starts
        print("game started ")

        while not game_over:
            # game starts. find image and take action
            img = ScreenCapture.get_screen(
                top = 160, left = 980, width = 600,
                height = 130, delay = 0
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
            top=135, left=1500, width=90, height=30, delay=0
        )
        try:
            score = int(game_vision.get_score(score_img))

        #score failed to be read, converted to int
        except Exception as e:

            with open('./errors/score_read.log', 'a+') as scoreFail:
                scoreFail.write(str(e))
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M', t)
            FILE_NAME = ("score_fail-" + timestamp)
            cv2.imwrite(
                r'./errors' + FILE_NAME + '.bmp', score_img
                )
            score = 42

        print('game done', score, '\n')

        return score

    def __len__(self):
        return 95100


def main():
    player = Player()
    sleep(2)
    player.play()


if __name__ == "__main__":
    main()
