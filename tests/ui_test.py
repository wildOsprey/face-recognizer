from PyQt5.QtTest import QTest
import unittest
import face_recognition
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication
from .main import FaceRecognition

def get_image(path):
    img= face_recognition.load_image_file(path) 
    return img

class UITest(unittest.TestCase):
    def test_click(self):
        app= QApplication(sys.argv)
        window = FaceRecognition()
        img = get_image(r'D:\repos\face_recognizer\tests\images\Aaron_Peirsol_0003.jpg')
        window.img = img
        okWidget = window.btRecognize
        QTest.mouseClick(okWidget, Qt.LeftButton)
        self.assertEqual(window.lblName.text(), 'Aaron Peirsol')
    

if __name__ == '__main__':
    unittest.main()