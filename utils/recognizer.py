import face_recognition
import cv2


class Recognizer():

    def __init__(self, db_manager, transform = None):
        '''
        Args:
            db_manager(DBManager): database manager which handles information with people and their encodings
            transform(func): transforms applied to the image before recognition
        '''
        super(Recognizer, self).__init__()
        self.db_manager = db_manager
        self.transform = None
        if transform:
            self.transform = transform



    def recognize(self, frame):
        '''
        Recognize people on the frame comparing them with database
        Args:
            frame(nparray): current frame
        '''
        if frame is None:
            raise Exception('You did not pass any image')
            
        if self.transform:
            frame = self.transform(frame)
        face_ids = []
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)
        clients = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            encodings = [enc['encoding'] for enc in self.db_manager.get_encodings()]
            
            ids = [enc['_id'] for enc in self.db_manager.get_ids()]

            matches = face_recognition.compare_faces(encodings, face_encoding)

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                _id = ids[first_match_index]
                face_ids.append(_id)
                clients.append( self.db_manager.get_client(_id))
            else:
                clients.append('Unknown')
        return clients, face_locations


    def draw_results(self, frame, face_locations, clients):
        '''
        Draws bounding boxes with predicted names on the frame
        Args:
            frame(nparray): current frame
            face_locations(list): locations of each face on the frame
            face_ids(list): ids of each person founded on the frame
        '''
        for (top, right, bottom, left), client in zip(face_locations, list(clients)):
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 10), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
        
            cv2.putText(frame, self.db_manager.get_fullname(client), (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
        return frame
