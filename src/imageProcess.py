import time
import cv2
import sys, os
from PIL import Image
import pytesseract
from matplotlib import pyplot as plt

sys.path.append("/../")
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
import numpy as np


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
        for templatePath in list_of_template_paths:
            # print(templatePath)

            self.templates[templatePath[27:-4]] = cv2.imread(
                templatePath, cv2.IMREAD_GRAYSCALE
            )
            # print(self.templates)
            # make sure all templates were read correctly
            ####NO CHECK CURRENTLY
        self.match_method = method
        self.dino_template = cv2.imread(dino_image_path, cv2.IMREAD_GRAYSCALE)
        # print(self.dino_template)
        self.dino_template_w, self.dino_template_h = self.dino_template.shape[::-1]

    @staticmethod
    def show_image(
        cv2_image,
    ):  # image should already be converted to the correct format
        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        cv2.imshow("OpenCV/Numpy grayscale", cv2_image),
        # cv2.cvtColor(converted_image, cv2.COLOR_BGRA2GRAY))

        cv2.waitKey(0)
        cv2.destroyAllWindows
        # Press "q" to quit
        # if (cv2.waitKey(1) & 0xFF == ord("q")):
        #     cv2.destroyAllWindows()
        #     break

    def find_dino(self, image, method=None, drawRect=False):

        result = cv2.matchTemplate(image, self.dino_template, self.match_method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

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
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        threshold = 0.9
        # print('maxval is: ', max_val)
        # print('max_loc is: ', max_loc)

        if max_val >= threshold:
            if drawRect:
                # get dimensions of template
                template_w, template_h = template.shape[::-1]

                # positions of best match
                top_left = max_loc
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
                # print("did not want to show rectangle\n")
                # place result into pipe or whatever. Or send to some getDistance() between dino and obstacle.

            return max_loc  # top left of the template found in the image

        else:
            pass
            # print('threshold of {} was not met, max_val was {}. \n'.format(threshold, max_val, ))

        return None  #####probably shouldnt be returning anything

    def get_distance(self, image, drawRect=False,):
        converted_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        x_diff = None
        y_diff = None
        obstacle_distances = {}
        dino_loc = self.find_dino(converted_image, drawRect=drawRect)
        for name, template in self.templates.items():

            obs_loc = self.find_obstacle(converted_image, template, drawRect=drawRect)

            if obs_loc != None:
                x_diff = obs_loc[0] - dino_loc[0]
                y_diff = obs_loc[1] - dino_loc[1]

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

                obstacle_distances[name] = (x_diff, y_diff)

            x_diff = None
            y_diff = None
            obs_loc = None

        if "game_over" in obstacle_distances.keys():
            return -1

        return obstacle_distances

    def get_score(self, image,):

        ret,thresh1 = cv2.threshold(image,127,255,cv2.THRESH_BINARY)

        # cv2.imshow('original image', image)
        # cv2.imshow('binary thresh', thresh1)
        # cv2.imshow('trunc thresh', thresh3)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # kernel = np.ones((2, 2), np.float32) / 3
        # dst = cv2.filter2D(image, -1, kernel)

        score = pytesseract.image_to_string(thresh1)
        # print(score)
        return score


    def createVideo(self, image, fileName):

        write_path = './test/image_recog/output/Nov-1-2020_1/'

        converted_image = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        x_diff = None
        y_diff = None
        obstacle_distances = {}
        dino_loc = self.find_dino(converted_image, drawRect=True)
        for name, template in self.templates.items():
            # print('name = ', name)
            obs_loc = self.find_obstacle(converted_image, template, drawRect=True)

            if obs_loc != None:
                x_diff = obs_loc[0] - dino_loc[0]
                y_diff = obs_loc[1] - dino_loc[1]

                p2 = (dino_loc[0] + x_diff, dino_loc[1] + y_diff)

                cv2.line(
                    converted_image,
                    dino_loc,
                    p2,
                    color=(0, 255, 0),
                    thickness=2,
                    lineType=cv2.LINE_4,
                )

                obstacle_distances[name] = (x_diff, y_diff)
                x_diff = None
                y_diff = None
                obs_loc = None

        # print('name = ', name)
        cv2.imwrite(write_path + fileName + '.bmp', converted_image)

        if "game_over" in obstacle_distances.keys():
            return -1

        return obstacle_distances
