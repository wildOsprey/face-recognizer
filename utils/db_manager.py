import face_recognition
import cv2
import glob
from pymongo import MongoClient
from bson import ObjectId
import os

def get_fullname(image_name):
    '''
    Get name of photo. Remove all numbers from it.
    '''
    base_name = os.path.basename(image_name)
    base_name = os.path.splitext(base_name)[0]
    clear_base_name = ''.join([i for i in base_name if not i.isdigit()]).split('_')
    name, surname = clear_base_name[0], clear_base_name[1]
    return name, surname

class DBManager():
    def __init__(self):
        super(DBManager, self).__init__()
        self.client = MongoClient('localhost', 27017)
        self.db = self.client["db"]
        self.clients = self.db["clients"]
        self.fill_collection()

    def get_collection(self):
        return self.clients.find({})

    def get_client(self, _id):
        return self.clients.find_one({'_id':ObjectId(_id)})

    def get_fullname(self, client):
        if client != 'Unknown':
            return client['name'] + ' ' + client['surname']
        else:
            return client

    def get_fullnames(self, clients):
        return [client['name'] + ' ' + client['surname']  if client != 'Unknown' else client for client in clients]

    def get_ids(self):
        return self.clients.find({}, { '_id':1})

    def get_encodings(self):
        return self.clients.find({}, { 'encoding':1, '_id':0})

    def get_clients(self, ids):
        return self.clients.find({ "_id": { "$in": ids }})

    def isExist(self, name, surname):
        return self.clients.find({"name": name, "surname": surname}).count() > 0

    def fill_collection(self):
        people = glob.glob("images/*.jpg")

        for person in people:
            # Load a second sample picture and learn how to recognize it.
            image = face_recognition.load_image_file(person)
            name, surname = get_fullname(person)

            if not self.isExist(name, surname):
                try:
                    encoding = face_recognition.face_encodings(image)[0]
                    mydict = { "name": name, "surname": surname, "img_path": person, "encoding": encoding.tolist() }
                    self.add_client(mydict)
                    print('Added')
                except:
                    print('Could not add to database')
                    continue
    
    #TODO validate distance 
    def add_client(self, client):
        try: 
            self.clients.insert_one(client)
        except:
            raise Exception('Could not add to database')


if __name__ == "__main__":
    db_manager = DBManager()


    