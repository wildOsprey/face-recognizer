import unittest
from .utils.recognizer import Recognizer
from .utils.db_manager import DBManager
import cv2
import face_recognition

def get_image(path):
    img= face_recognition.load_image_file(path) 
    return img

class Test(unittest.TestCase):
    def test_recognize_one(self):
        db_manager = DBManager()
        recognizer = Recognizer(db_manager)
        img = get_image('tests//images//Vladimir_Meciar_0001.jpg')
        people, _= recognizer.recognize(img)
        self.assertEqual(len(people), 1)
        self.assertEqual(db_manager.get_fullname(people[0]), 'Vladimir Meciar')
        self.assertNotEqual(db_manager.get_fullname(people[0]), 'Vince Carter')
        
    def test_recognize_many(self):
        db_manager = DBManager()
        recognizer = Recognizer(db_manager)
        img = get_image('tests//test_many.jpg')
        people, boxes= recognizer.recognize(img)
        self.assertEqual(len(boxes), 4)
        self.assertEqual(len(people), 4)
        self.assertNotEqual(db_manager.get_fullname(people[0]), 'Vladimir Meciar')
        self.assertNotEqual(db_manager.get_fullname(people[1]), 'Vince Carter')
        self.assertEqual(db_manager.get_fullname(people[0]), 'Unknown')
        self.assertEqual(db_manager.get_fullname(people[1]), 'Alexandra Mishchenko')
        self.assertEqual(db_manager.get_fullname(people[2]), 'Unknown')
        self.assertEqual(db_manager.get_fullname(people[3]), 'Dmitro Sylenok')

    def test_recognize_no_one(self):
        db_manager = DBManager()
        recognizer = Recognizer(db_manager)
        self.assertRaises(Exception, recognizer.recognize, None)


if __name__ == '__main__':
    unittest.main()