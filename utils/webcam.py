import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap
import cv2
from PyQt5.QtCore import QTimer

class ImageWidget():
    def __init__(self, label):
        #type: (QLabel)
        super(ImageWidget, self).__init__()
        self.image = None
        self.label = label

    def displayImage(self, img, window=1):
        '''
        Preprocess image and displays it on label.
        Args:
            img(array): img to display
        '''  
        qformat = QImage.Format_Indexed8
        if len(img.shape) == 3:
            if img.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(img, img.shape[1],
                          img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if window == 1:
            self.label.setPixmap(QPixmap.fromImage(outImage))
            self.label.setScaledContents(True)


class WebCam(ImageWidget):
    def __init__(self, label, timer, preprocess=None):
        #type: (QLabel, QTimer, func)
        super(WebCam, self).__init__(label)
        self.timer = timer
        self.preprocess = preprocess

    def start(self):
        '''
            Initialize capturing from webcam and start timer,
            which updates frame on each tick.
        '''
        self.capture = cv2.VideoCapture(0)
        #width, height = self.label.width, self.label.height
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 237)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)


    def update_frame(self):
        '''
        Updates each frame with some preprocessing (adding boxes and names on the frame)
        and displays it.
        '''
        ret, self.image = self.capture.read()
        self.image = cv2.flip(self.image, 1)
        if self.preprocess:
            self.image = self.preprocess(self.image)
        super(WebCam, self).displayImage(self.image, 1)



    def stop(self):
        '''
        Stops videostream.
        '''
        self.timer.stop()
