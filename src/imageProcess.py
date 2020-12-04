import time, cv2, sys, os
from datetime import datetime
from PIL import Image
import pytesseract
from matplotlib import pyplot as plt
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"


class ImageProcess:
    def __init__(
        self,
        list_of_template_paths,
        dino_image_path,
        method=cv2.TM_CCOEFF_NORMED,
        **kwargs
    ):
        """list of template paths to use matchTemplate on. Must do if there is intent of using match template

        Args:
            list_of_template_paths (list): list of file paths of the images to use as templates.
        """
        self.templates = {}

        self.obsNameList = list(map(
            lambda x: os.path.splitext(os.path.basename(x))[0],
            list_of_template_paths
        ))

        #assume list(map) is ordered
        #thus both obsNameList and
        #list_of_template_paths are in
        #the same order
        for i in range(len(list_of_template_paths)):

            self.templates[self.obsNameList[i]] = cv2.imread(
                list_of_template_paths[i], cv2.IMREAD_GRAYSCALE
            )

        self.match_method = method
        self.dino_template = cv2.imread(dino_image_path, cv2.IMREAD_GRAYSCALE)
        self.dino_template_w, self.dino_template_h = self.dino_template.shape[::-1]
        self.dino_misses = 0

    def get_obs_names(self):
        return self.obsNameList

    @staticmethod
    def show_image(cv2_image):
        # image should already be converted to the correct format
        # Display the picture in grayscale
        cv2.imshow("image", cv2_image),
        cv2.waitKey(0)
        cv2.destroyAllWindows

    def find_dino(self, image, method=None, drawRect=False):

        result = cv2.matchTemplate(image, self.dino_template, self.match_method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        #if dinosaur is in frame, continue.
        #Else do nothing as distances cannot be computed
        if max_val > 0.7:
            pass
        else:
            return None

        bottom_right = (
            max_loc[0] + self.dino_template_w,
            max_loc[1] + self.dino_template_h,
        )

        if drawRect:
            cv2.rectangle(
                image,
                max_loc,
                bottom_right,
                color=(0, 255, 0),
                thickness=2,
                lineType=cv2.LINE_4,
            )
            # self.show_image(image)

        # print(bottom_right)
        return (
            bottom_right  # use bottom right corner to find distance from dino to object
        )

    def find_obstacle(self, converted_image, template, method=None,
                        drawRect=False):

        result = cv2.matchTemplate(converted_image, template, self.match_method)
        # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.9
        # print('maxval: {}\n'.format(max_val))

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        if locations:

            if drawRect:
                # get dimensions of template
                template_w, template_h = template.shape[::-1]

                # positions of best match
                top_left = locations[0]
                bottom_right = (top_left[0] + template_w, top_left[1] + template_h)

                cv2.rectangle(
                    converted_image,
                    top_left,
                    bottom_right,
                    color=(0, 255, 0),
                    thickness=2,
                    lineType=cv2.LINE_4,
                )
                # self.show_image(converted_image)

            else:
                pass

            return locations  # top left of the template found in the image

        else:
            pass
            # print('threshold of {} was not met, max_val was {}. \n'.format(threshold, max_val, ))

        return None

    #finds dino location in addition to obstacles
    #can be useful for video but pretty useless
    #for actual gameplay
    def get_distance_DEPRECATED(self, image, drawRect=False,):
        converted_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        x_diff = None
        y_diff = None
        obstacle_distances = {}
        dino_loc = self.find_dino(converted_image, drawRect=drawRect)
        print('dino_loc = ({}, {})'.format(dino_loc[0], dino_loc[1]))
        for name, template in self.templates.items():
            print('obs is: ', name)
            obs_locations = self.find_obstacle(
                converted_image,
                template,
                drawRect=drawRect
            )

            #list of obstacles returned
            if obs_locations:
                for i, location in enumerate(obs_locations):
                    x_diff = location[0] - dino_loc[0]
                    y_diff = location[1] - dino_loc[1]

                    p2 = (dino_loc[0] + x_diff, dino_loc[1] + y_diff)

                    if drawRect == True:
                        cv2.line(
                            converted_image,
                            dino_loc,
                            p2,
                            color=(0, 255, 0),
                            thickness=2,
                            lineType=cv2.LINE_4,
                        )
                        self.show_image(converted_image)

                    obstacle_distances[
                        name + '_{}'.format(str(i))
                        ] = (x_diff, y_diff)

                    x_diff = None
                    y_diff = None
                    obs_loc = None

        if 'game_over_0' in obstacle_distances.keys():
            return -1

        return obstacle_distances

    def get_distance(self, image, drawRect=False,):
        converted_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        obstacle_distances = {}

        for name, template in self.templates.items():
            # print('obs is: ', name)
            obs_locations = self.find_obstacle(
                converted_image,
                template,
                drawRect=drawRect
            )

            #list of obstacles returned
            if obs_locations:
                for i, location in enumerate(obs_locations):
                    x_pos = location[0]
                    y_pos = location[1]

                    obstacle_distances[
                        name + '_{}'.format(str(i))
                        ] = (x_pos, y_pos)

        if "game_over_0" in obstacle_distances.keys():
            return -1

        #get closest obstacle and return its distance
        if obstacle_distances:
            closest_obs = sorted(
                obstacle_distances.items(),
                key= lambda x: x[1]
            )
            closest_obs = closest_obs[0]

            return closest_obs

        else:
            return None

    def get_score(self, image, show_score = False):

        ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)

        if show_score:
            # cv2.imshow('original image', image)
            cv2.imshow('binary thresh', thresh1)
            # cv2.imshow('trunc thresh', thresh3)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # kernel = np.ones((2, 2), np.float32) / 3
        # dst = cv2.filter2D(image, -1, kernel)

        score = pytesseract.image_to_string(thresh1)
        if 'o' in score:
            score.replace('o', '0')
        # print(score)
        return score


    def createVideo(self, image, fileName):

        write_path = './video_output/Nov-30-2020/'

        converted_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        x_diff = None
        y_diff = None
        obstacle_distances = {}
        dino_loc = self.find_dino(converted_image, drawRect=True)


        #check if dino in frame
        if dino_loc:
            self.dino_misses = 0
            pass
        else:
            cv2.imwrite(fileName, converted_image)
            self.dino_misses += 1
            if self.dino_misses >= 25:
                return -1
            else:
                return None

        for name, template in self.templates.items():
            obs_locs = self.find_obstacle(
                converted_image,
                template,
                drawRect=True
            )

            if obs_locs != None:
                for i, (x_dist, y_dist) in enumerate(obs_locs):
                    x_diff = x_dist - dino_loc[0]
                    y_diff = y_dist - dino_loc[1]

                    p2 = (dino_loc[0] + x_diff, dino_loc[1] + y_diff)

                    cv2.line(
                        converted_image,
                        dino_loc,
                        p2,
                        color=(0, 255, 0),
                        thickness=2,
                        lineType=cv2.LINE_4,
                    )

                    obstacle_distances[
                        name + '_{}'.format(str(i))
                        ] = (x_dist, y_dist)

                    x_diff = None
                    y_diff = None
                    obs_loc = None

        ret = cv2.imwrite(fileName, converted_image)
        # print('ret is ', ret)
        if "game_over_0" in obstacle_distances.keys():
            return -1

        #get closest obstacle and return its distance
        elif obstacle_distances:
            closest_obs = sorted(
                obstacle_distances.items(),
                key= lambda x: x[1]
            )
            closest_obs = closest_obs[0]

            return closest_obs

        else:
            return None
