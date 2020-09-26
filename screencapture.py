import cv2
import numpy as np
from mss.windows import MSS as mss 
from pynput.mouse import Button, Controller

class windowCapture:

    def __init__(self):
        self._image = None
    
    def show_image(self):
        self._image.show()

    def save_image(self, fileName):
        self._image.save(fileName, format="png")

    @staticmethod
    def list_windows_names():
        def winEnumHandler( hwnd, ctx ):
            if win32gui.IsWindowVisible( hwnd ):
                print (hex(hwnd), win32gui.GetWindowText( hwnd ))

        win32gui.EnumWindows( winEnumHandler, None )

    @staticmethod
    def get_screen():
        with mss() as sct:
            monitor = {"top": 40, "left": 0, "width": 800, "height": 640}
            while "Screen capturing":
                last_time = time()

                # Get raw pixels from the screen, save it to a Numpy array
                img = numpy.array(sct.grab(monitor))

                # Display the picture
                # cv2.imshow("OpenCV/Numpy normal", img)

                # Display the picture in grayscale
                cv2.imshow('OpenCV/Numpy grayscale', 
                        cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))

                print("fps: {}".format(1 / (time() - last_time)))

                # Press "q" to quit
                if (cv2.waitKey(1) & 0xFF == ord("q")):
                    cv2.destroyAllWindows()
                    break
        return
















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