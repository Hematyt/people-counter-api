import cv2
import numpy as np
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

#img = cv2.imread('images/droga.jpg')
#cv2.imshow('image', img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()pokazuje zdjecie


class PeopleCounter(Resource):
    def get(selfself):
        img = cv2.imread('images/droga.jpg')
        boxes, weights = hog.detectMultiScale(img, winStride=(2,2))
        print(type(img))
        print(img.shape)
        return {'count': len(boxes)}


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_resource(HelloWorld, '/test')
api.add_resource(PeopleCounter, '/people')

if __name__ == '__main__':
    app.run(debug=True)   # można dodać port =80, 443, etc
