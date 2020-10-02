import cv2
import numpy as np

facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
font = cv2.FONT_HERSHEY_SIMPLEX

class VideoCamera(object):
    def __init__(self, f_path):
        self.video = cv2.VideoCapture(f_path)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        self.count = 0

    def __del__(self):
        self.video.release()

    # returns camera frames along with bounding boxes and predictions
    def get_frame(self):
        _, fr = self.video.read()
        gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        faces = facec.detectMultiScale(gray_fr, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
        _, jpeg = cv2.imencode('.jpg', fr)
        
        # face_file_name = "face/" + str(y) + ".jpg"
        cv2.imwrite("static/frames/%d.jpg" % self.count, fr)
        self.count = self.count + 1
        return (jpeg.tobytes())
