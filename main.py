import sys

from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap, QRegExpValidator
import cv2
from PyQt5.QtCore import QTimer, QRegExp
from utils.webcam import WebCam, ImageWidget
from utils.db_manager import DBManager
from utils.recognizer import Recognizer
import face_recognition

noname_img = 'ui/images/noname.jpg'

def transform(frame):
    #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = frame[:, :, ::-1]
    return rgb_small_frame

class DataDialog(QDialog):
    def __init__(self, parent, img, db_manager):
        super().__init__(parent)
        loadUi('ui/db_window.ui', self)
        self.photo = ImageWidget(self.lblPhoto)
        self.img = img
        self.photo.displayImage(self.img)
        self.db_manager = db_manager
        self.btSaveToDB.clicked.connect(self.save_to_db)
        regexp = QRegExp('[A-Za-z]{2,30}')
        self.txtName.setValidator(QRegExpValidator(regexp))
        self.txtSurname.setValidator(QRegExpValidator(regexp))

    def show_msg(self, text, title):
        msg = QMessageBox()
        msg.setText(text)
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.show()
        retval = msg.exec_()
        
    def save_to_db(self):
        if self.validate_fields():
            name = self.txtName.text()
            surname = self.txtSurname.text()
            fullname = name + '_' + surname
            img_path = 'tests/images/' + fullname + '.jpg'
            if self.db_manager.isExist(name, surname):
                self.show_msg("Your name is already in the database. Consider choosing another one. Ex. Catastrophe", "Attention!")
                return 
            cv2.imwrite(img_path, self.img)
            image = face_recognition.load_image_file(img_path)
            encoding = face_recognition.face_encodings(image)[0]
            mydict = { "name": name, "surname": surname, "img_path": img_path, "encoding": encoding.tolist() }
            self.db_manager.add_client(mydict)
            self.done(1)

    def validate_fields(self):
        if self.txtName.text() == "" or self.txtSurname.text() == "":
            self.show_msg("Enter your name and surname, please.", "You make me fill sad..")
            return False
        return True


class FaceRecognition(QMainWindow):
    def __init__(self):
        super(FaceRecognition, self).__init__()
        loadUi('ui/main.ui', self)

        self.webcam = WebCam(self.lblCamera, QTimer(self), self.recognize_each_frame)
        self.webcam.start()

        self.db_manager = DBManager()
        self.recognizer = Recognizer(self.db_manager, transform)
        self.btRecognize.clicked.connect(self.recognize)
        self.btAddToDB.clicked.connect(self.add_to_db)

        self.lblres = ImageWidget(self.lblResult)
        self.img = None
        self.clear_result_fields()
        self.btReset.clicked.connect(self.clear_result_fields)

    '''
    Args:
        img(array): current frame
    Is called by WebCam object each frame.
    Updates img field so that we can access it in other methods of class.
    Returns:
        If display box is checked, recognize and draws box and person data on frame.
        If not, return img without any transforms.
    '''
    def recognize_each_frame(self, img):
        self.img = img
        if self.img is None:
            self.clear_result_fields()
            return

        if self.btDisplay.isChecked():
            clients, locations = self.recognizer.recognize(self.img)
            clients = list(clients)
            img = self.recognizer.draw_results(img, locations, clients)

        return img

    '''
    Do recognition on the frame at specific moment of time. 
    Updates results fields.
    '''
    def recognize(self):
        #clear fields
        self.clear_result_fields()

        #do recognition
        clients, _ = self.recognizer.recognize(self.img)
        clients = list(clients)

        self.btReset.setEnabled(True)

        #if no match - person is Unknown.
        if len(clients) == 0:
            self.fill_result_fields('Unknown', noname_img)
            return 

        #get first founded result (expected to have only one person on frame)
        self.fill_result_fields(self.db_manager.get_fullname(clients[0]), clients[0]['img_path'])

    def add_to_db(self):
        self.widget = DataDialog(self, self.img, self.db_manager)
        self.widget.show()

    def clear_result_fields(self):
        self.btReset.setEnabled(False)
        self.fill_result_fields('', noname_img)

    def fill_result_fields(self, text, path):
    #type: (string, string)
        self.lblName.setText(text)
        img = cv2.imread(path)
        self.lblres.displayImage(img)

if __name__=='__main__':
    app= QApplication(sys.argv)
     
    window = FaceRecognition()
    
    window.setWindowTitle('Face recognition')
    window.show()
    sys.exit(app.exec_())