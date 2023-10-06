import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLabel, QFileDialog, QApplication, QScrollArea
from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QImage
import numpy as np
from PIL import Image, ImageOps
import math


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("image.ui", self)
        
        self._image_button = self.findChild(QPushButton, "pushButton")
        self._convert_button = self.findChild(QPushButton, "pushButton_2")
        self._image = self.findChild(QLabel, "label")
        self._scroll_area = self.findChild(QScrollArea, "scrollArea")

        self._image_button.clicked.connect(self.open_image)
        self._convert_button.clicked.connect(self.transform)

        self.show()
    
    def open_image(self):

        fname = QFileDialog.getOpenFileName(self, "Open File", "c:", "Images (*.jpg)")
        try:
            self._pil_image = Image.open(fname[0])
        except AttributeError:
            return

        self._pixmap = QPixmap(fname[0])

        self._image.setPixmap(self._pixmap)

    def transform(self):
        try:
            size = self._pixmap.size()
            arr = self.generate_sobel_array()
            h, w = size.height(), size.width()
            q_img = QImage(arr,w,h,w,QImage.Format_Grayscale8)
            self._pixmap = QPixmap.fromImage(q_img)
            self._image.setPixmap(self._pixmap)
        except AttributeError:
            return

    def generate_sobel_array(self) -> np.array:
        size = self._pixmap.size()
        gray_im = ImageOps.grayscale(self._pil_image)
        numpydata = np.asarray(gray_im).copy()

        arr = numpydata

        xKernel = np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        yKernel = np.array([[-1,-2,-1],[0,0,0],[1,2,1]])

        for y in range(1, size.height()-3):
            for x in range(1, size.width()-3):

                gx = np.sum(np.multiply(arr[y-1:y+2, x-1:x+2], xKernel))
                gy = np.sum(np.multiply(arr[y-1:y+2, x-1:x+2], yKernel))

                g = math.sqrt(gx ** 2 + gy ** 2) 

                if(g>255):
                    g = 255
                elif(g<0):
                    g = 0

                arr[y-1][x-1] = g
        return arr
    
        '''
        #Attempted to apply linear filters, does not work as intended

        horizontal_x = arr[:,2:] - arr[:,:-2]
        gx = horizontal_x[:-2] + horizontal_x[2:] + 2*horizontal_x[1:-1]

        horizontal_y =  arr[:,2:] + arr[:,:-2] + 2*arr[:,1:-1]       
        gy = horizontal_y[2:,:] - horizontal_y[:-2,:]     
                                              

        for y in range(1, size.height()-3):
            for x in range(1, size.width()-3):
                x_val = gx[y][x]
                y_val = gy[y][x]
                g = math.sqrt(x_val ** 2 + y_val ** 2)

                if(g>255):
                    g = 255
                elif(g<0):
                    g = 0
                arr[y-1][x-1] = g
        
        return arr
        '''

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec_()



