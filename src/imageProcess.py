import time
import cv2
import sys, os
sys.path.append('/../')

##check to make sure filepaths and imports are working correctly
# test = cv2.imread('images/templates/double_cactus_small.PNG')
# cv2.imshow('OpenCV/Numpy grayscale',
#         cv2.cvtColor(test, cv2.COLOR_BGRA2GRAY))
# cv2.waitKey(0)
# cv2.destroyAllWindows


class imageProcess:

    def __init__(self, list_of_template_paths, method = cv2.TM_CCOEFF_NORMED):
        """list of template paths to use matchTemplate on. Must do if there is intent of using match template

        Args:
            list_of_template_paths (list): list of file paths of the images to use as templates.
        """
        self.templates = []
        for templatePath in list_of_template_paths:
            print(templatePath)
            self.templates.append(cv2.imread(templatePath, cv2.IMREAD_GRAYSCALE))

        #make sure all templates were read correctly
        ####NO CHECK CURRENTLY

        self.match_method = method


    @staticmethod
    def show_image(cv2_image): #image should already be converted to the correct format
        # Display the picture
        # cv2.imshow("OpenCV/Numpy normal", img)

        # Display the picture in grayscale
        cv2.imshow('OpenCV/Numpy grayscale', cv2_image),
                #cv2.cvtColor(np_image_array, cv2.COLOR_BGRA2GRAY))


        cv2.waitKey(0)
        cv2.destroyAllWindows
        # Press "q" to quit
        # if (cv2.waitKey(1) & 0xFF == ord("q")):
        #     cv2.destroyAllWindows()
        #     break


    def find_match(self, np_image_array, method = None, drawRect = False):
        for template in self.templates:

            result = cv2.matchTemplate(np_image_array, template, self.match_method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            threshold = 0.9
            print('maxval is: ', max_val)

            if max_val >= threshold:
                if drawRect:
                    #get dimensions of template
                    template_w, template_h = template.shape[::-1]

                    #positions of best match
                    top_left = max_loc
                    bottom_right = (top_left[0] + template_w, top_left[1] + template_h)

                    cv2.rectangle(np_image_array, top_left, bottom_right,
                                    color = (0, 255, 0), thickness= 2, lineType=cv2.LINE_4)

                    self.show_image(np_image_array)
                else:
                    print("did not want to show rectangle\n")
            else:
                print('threshold of {} was not met, max_val was {}.'.format(threshold, max_val, ))



        return result
