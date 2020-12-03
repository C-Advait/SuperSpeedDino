from pyautogui import press, keyDown, keyUp
from imageProcess import ImageProcess
from screencapture import ScreenCapture
from time import sleep
import sys, os, random, threading, re, time, copy
import logging, cv2, string, shutil
from pprint import pprint
import numpy as np
sys.path.append("/../")

class Player2D:

    def __init__(self, create_info = True):
        self.score = None
        self.identifier = ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=9))

        # Create image processing object to use detection with
        template_files = os.listdir("images/obstacle_images")
        for index, fileName in enumerate(template_files):
            template_files[index] = "images/obstacle_images/" + fileName
        dinosaur_image_path = r"images/dinosaur.PNG"

        self.game_vision= ImageProcess(template_files, dinosaur_image_path)

        self.obs_names = self.game_vision.get_obs_names()

        try:
            self.obs_names.remove('game_over')
        except ValueError:
            pass

        self.decisionGenes = { name: None for name in self.obs_names}
        # print(self.decisionGenes)

        for key in self.decisionGenes.keys():
            self.decisionGenes[key] = np.empty([650,100], dtype=object)

        logging.basicConfig(
            filename='play_excepts.log',
            filemode='w',
            format='%(name)s - %(levelname)s - %(message)s'
        )

        if create_info:
            self.create_genetic_info()

    # press up key for `time` seconds
    def jump(self, time, keypressMut):
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

    # press the down key for `time` seconds
    def duck(self, time, keypressMut):

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

    def noneTest(self):
        for key in self.decisionGenes:
            for x_list in self.decisionGenes[key]:
                for y in x_list:
                    if None in y:
                        print('key: ', key)

    @staticmethod
    def copy_player(individual):
        new_player = Player(create_info=False)
        for key in individual.decisionGenes:
            new_player.decisionGenes[key] = copy.deepcopy(
                individual.decisionGenes[key]
            )

        return new_player


    def play(self):

        keypressMut = threading.Lock()
        pattern = re.compile('_\d+')
        game_over = False

        time.sleep(1) #game actually resets
        press("space")  # start game
        time.sleep(0.5) #game starts
        print("game started ")

        while not game_over:
            # game starts. find image and take action
            img = ScreenCapture.get_screen(
                top = 172, left = -1543, width = 600,
                height = 125, delay = 0.4
            )
            res = self.game_vision.get_distance(img)
            if res:
                # print(res)
                try:
                    obstacle, distance = res
                    match = pattern.search(obstacle)

                    obs_name = obstacle[:match.span()[0]]
                    action, wait = self.decisionGenes[obs_name][distance[0]][distance[1]]
                    if action == None:
                        print(action, wait, distance[0], distance[1])
                        raise IndexError
                    action(wait, keypressMut)

                #res = -1
                except TypeError as e:
                    game_over = True

        score_img = ScreenCapture.get_screen(
            top=142, left= -1009, width=65, height=20, delay=0
        )
        try:
            score = int(self. game_vision.get_score(score_img))

        #Score could not be converted to int
        #Issue with OCR software
        except ValueError as e:
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


class Player1D(Player2D):

    def __init__(self):
        self.score = None
        self.identifier = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=9))

        # Create image processing object to use detection with
        template_files = os.listdir("images/obstacle_images")
        for index, fileName in enumerate(template_files):
            template_files[index] = "images/obstacle_images/" + fileName
        dinosaur_image_path = r"images/dinosaur.PNG"

        self.game_vision= ImageProcess(template_files, dinosaur_image_path)

        self.obs_names = self.game_vision.get_obs_names()

        try:
            self.obs_names.remove('game_over')
        except ValueError:
            pass

        self.decisionGenes = { name: None for name in self.obs_names}

        for key in self.decisionGenes.keys():
            self.decisionGenes[key] = np.empty(400, dtype=object)

        logging.basicConfig(filename='play_excepts.log', \
            filemode='w', format='%(name)s - %(levelname)s - %(message)s')

        self.create_genetic_info()

    def get_identifier(self):
        return self.identifier

    def set_identifier(self, new_identifier):
        self.identifier = new_identifier

    def update_identifier(self):
        self.identifier = ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=9))

    def create_genetic_info(self):

        #ground obstacles can only be jumped over
        #bird can be ducked or jumped over
        ground_obs_actions = [self.jump, self.do_nothing]
        bird_obs_actions = [self.jump, self.do_nothing, self.duck]


        for key in self.decisionGenes.keys():
            if 'bird' not in key:
                for i in range(len(self.decisionGenes[key])):
                    randSleep = random.uniform(0.1, 1.5)

                    self.decisionGenes[key][i] = [
                        random.choice(ground_obs_actions),
                        randSleep
                    ]
            else:
                for i in range(len(self.decisionGenes[key])):
                    randSleep = random.uniform(0.1, 1.5)

                    self.decisionGenes[key][i] = [
                        random.choice(bird_obs_actions),
                        randSleep
                    ]

    def play(self):

        keypressMut = threading.Lock()
        pattern = re.compile('_\d+')
        game_over = False

        time.sleep(1) #game resets
        press("space")  # start game
        time.sleep(0.5) #game starts

        while not game_over:
            # game starts. find image and take action
            img = ScreenCapture.get_screen(
                top = 172, left = -1524, width = 400,
                height = 125, delay = 0
            )
            res = self.game_vision.get_distance(img)
            if res:
                try:
                    obstacle, (x_dist, y_dist) = res
                    match = pattern.search(obstacle)
                    obs_name = obstacle[:match.span()[0]]
                    action, wait = self.decisionGenes[obs_name][x_dist]
                    action(wait, keypressMut)

                #res = -1
                except TypeError as e:
                    game_over = True

        score_img = ScreenCapture.get_screen(
            top=142, left= -1009, width=65, height=20, delay=0
        )
        try:
            score = int(self.game_vision.get_score(score_img))

        #Score could not be converted to int
        #Issue with OCR software
        except ValueError as e:
            with open('./errors/score_read.log', 'a+') as scoreFail:
                scoreFail.write(str(e))
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M', t)
            FILE_NAME = (timestamp)
            cv2.imwrite(
                r'./errors/' + FILE_NAME + '.bmp', score_img
            )
            score = 42

        # print('game done', score, '\n')

        return score

    def play_with_video(self):
        keypressMut = threading.Lock()
        pattern = re.compile('_\d+')
        game_over = False
        folderName = f'video_output/Dec-02-2020/{self.identifier}'
        try:
            os.makedirs(folderName)
        except OSError as e:
            logging.log(level=Warning, msg=e)

        counter = 0

        time.sleep(1) #game resets
        press("space")  # start game
        time.sleep(0.5) #game starts

        while not game_over:
            # game starts. find image and take action
            img = ScreenCapture.get_screen(
                top = 172, left = -1524, width = 400,
                height = 125, delay = 0
            )
            res = self.game_vision.createVideo(img, \
                folderName + f'/{counter}.bmp')
            counter += 1
            if res:
                try:
                    obstacle, (x_dist, y_dist) = res
                    match = pattern.search(obstacle)
                    obs_name = obstacle[:match.span()[0]]
                    action, wait = self.decisionGenes[obs_name][x_dist]
                    action(wait, keypressMut)

                #res = -1
                except TypeError as e:
                    game_over = True

        score_img = ScreenCapture.get_screen(
            top=142, left= -1009, width=65, height=20, delay=0
        )
        try:
            score = int(self.game_vision.get_score(score_img))

        #Score could not be converted to int
        #Issue with OCR software
        except ValueError as e:
            with open('./errors/score_read.log', 'a+') as scoreFail:
                scoreFail.write(str(e))
            t = time.localtime()
            timestamp = time.strftime('%b-%d-%Y_%H%M', t)
            FILE_NAME = (timestamp)
            cv2.imwrite(
                r'./errors/' + FILE_NAME + '.bmp', score_img
            )
            score = 42

        # print('game done', score, '\n')

        return score

    def __len__(self):
        return 400


def main():
    player = Player1D()
    sleep(2)
    player.play_with_video()
    # pprint(player.decisionGenes['single_cactus_small'][0][0])

if __name__ == "__main__":
    main()
