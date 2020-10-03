import time
import cv2
import sys, os
sys.path.append('/../images/templates/')

class imageProcess:

    def __init__(list_of_template_paths, method = ):
        """list of template paths to use matchTemplate on. Must do if there is intent of using match template

        Args:
            list_of_template_paths (list): list of file paths of the images to use as templates.
        """
        self.templates = []
        for templatePath in list_of_template_paths:
            self.templates.append(cv2.imread(templatePath))


    @staticmethod
    def show_image(np_image_array):
        last_time = time.time()
        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        cv2.imshow('OpenCV/Numpy grayscale',
                cv2.cvtColor(np_image_array, cv2.COLOR_BGRA2GRAY))

        print("fps: {}".format(1 / (time.time() - last_time)))

        cv2.waitKey(0)
        cv2.destroyAllWindows
        # Press "q" to quit
        # if (cv2.waitKey(1) & 0xFF == ord("q")):
        #     cv2.destroyAllWindows()
        #     break

    
    def find_match(self, method = None, np_image_array):

