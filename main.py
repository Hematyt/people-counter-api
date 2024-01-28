import cv2
from flask import Flask, request
from flask_restful import Resource, Api
from urllib.request import urlopen
import numpy as np


app = Flask(__name__)
api = Api(app)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


class PeopleCounter(Resource):
    def get(self):
        img = cv2.imread('images/droga.jpg')
        boxes, weights = hog.detectMultiScale(img, winStride=(4,4))
        return {'count': len(boxes)}


class PeopleCounter2(Resource):
    def get(self):
        img_url = request.args.get('img_url')   #np http://127.0.0.1:5000/?img_url=https://rzeszow-news.pl/wp-content/uploads/sites/1/nggallery/prezentacja-dworzec-pks-pazdziernik-2021/pks-03-wiz-1920x1080.jpg
        resp = urlopen(img_url)
        img2 = np.asarray(bytearray(resp.read()), dtype="uint8")
        img2 = cv2.imdecode(img2, cv2.IMREAD_COLOR)
        boxes, weights = hog.detectMultiScale(img2, winStride=(4, 4))
        return {'count': len(boxes)}





api.add_resource(PeopleCounter, '/people')
api.add_resource(PeopleCounter2, '/')

if __name__ == '__main__':
    app.run(debug=True)
