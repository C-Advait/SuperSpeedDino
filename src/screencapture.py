import cv2
import numpy as np
from mss.windows import MSS as mss
from pynput import mouse
import time

class ScreenCapture:

    def __init__(self):
        self._image = None

    def show_image(self):
        self._image.show()

    def save_image(self, fileName):
        self._image.save(fileName, format="png")


    @staticmethod
    def get_screen(top = 300, left = 600, width = 700, height = 200, continuousRun = False, queue = None):
        """Get np.array of the screen area specified.

        Args:
            top (int, optional): y position, upper left hand corner. Measured from top left of screen. Defaults to 300.
            left (int, optional): x position, upper left hand corner. Measured from top left of screen. Defaults to 600.
            width (int, optional): x offset from 'left' to capture. Width of image. Defaults to 700.
            height (int, optional): y offset from 'top' to capture. Height of image. Defaults to 200.

            OTHER PARAMS NOT DESCRIBED ATM

        Returns:
            np.array: np.arry of pixels on screen. Captured using mss() library
        """
        with mss() as sct:
            monitor = {"top": top, "left": left, "width": width, "height": height}
            time.sleep(5) #open game window in this time frame
            while continuousRun:
                img = np.array(sct.grab(monitor))

                #queue.put(img) #implement later
            else:
                img = np.array(sct.grab(monitor))
                return img

        raise EOFError('should never have gotten here')


"""
    @staticmethod
    def get_image_box():
        def on_click(x, y, button, pressed):
            global num_clicks
            print('{0} at {1}'.format(
                'Pressed' if pressed else 'Released',
                (x, y)))
            num_clicks += 1
            if num_clicks == 2:
                # Stop listener
                del num_clicks
                return False


        with mouse.Listener(on_click=on_click) as listener:
            listener.join()
"""




















    # @staticmethod
    # def get_screen():
    #     w = 1200
    #     h = 720

    #     # hwnd = win32gui.FindWindow(None, screenName)
    #     hwnd = None

    #     wDC = win32gui.GetWindowDC(hwnd)
    #     dcObj = win32ui.CreateDCFromHandle(wDC)
    #     cDC = dcObj.CreateCompatibleDC()
    #     dataBitMap = win32ui.CreateBitmap()
    #     dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    #     cDC.SelectObject(dataBitMap)
    #     cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

    #     signedIntsArray = dataBitMap.GetBitmapBits(True)
    #     img = np.fromstring(signedIntsArray, dtype='uint8')
    #     img.shape = (h, w, 4)
    #     #dont want to save to a literal file
    #     #dataBitMap.SaveBitmapFile(cDC, bmpfilenamename)

    #     # Free Resources
    #     dcObj.DeleteDC()
    #     cDC.DeleteDC()
    #     win32gui.ReleaseDC(hwnd, wDC)
    #     win32gui.DeleteObject(dataBitMap.GetHandle())

    #     img = np.array(img)
    #     img = cv2.cvtColor(img, 1)
    #     return img