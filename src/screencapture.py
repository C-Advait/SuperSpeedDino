import cv2
import numpy as np
from mss.windows import MSS as mss
from tkinter import Tk, Button, W
import win32api
import time


class ScreenCapture:
    def __init__(self):
        self._image = None

    def show_image(self):
        self._image.show()

    def save_image(self, fileName):
        self._image.save(fileName, format="png")


    @staticmethod
    def cursorPos():
        def enable_mouseposition():
            window.after(10, get_mouseposition)


        def get_mouseposition():
            state_left = win32api.GetKeyState(0x01)
            if state_left == -127 or state_left == -128:
                xclick, yclick = win32api.GetCursorPos()
                print(xclick, yclick)
            else:
                window.after(10, get_mouseposition)

        window = Tk()
        window.geometry("700x500")
        window.title("Testing")

        b = Button(window, text="OK", command=enable_mouseposition)
        b.grid(row=0, column=2, sticky=W)
        quit_b = Button(window, text="Quit", command=window.destroy)
        quit_b.grid(row = 20, column = 20, sticky = W)

        window.mainloop()


    @staticmethod
    def get_screen(
        top=300,
        left=600,
        width=700,
        height=200,
        continuousRun=False,
        queue=None,
        delay=5,
    ):
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

            if delay:
                time.sleep(delay)  # open game window in this time frame

            while continuousRun:
                img = np.array(sct.grab(monitor))

                # queue.put(img) #implement later
            else:
                img = np.array(sct.grab(monitor))
                return img

        raise EOFError("should never have gotten here")
