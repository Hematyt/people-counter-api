import cv2
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from urllib.request import urlopen
import numpy as np
import os
from flask.views import MethodView

app = Flask(__name__, template_folder='templates')
api = Api(app)

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


def count_people(image_path):
    img = cv2.imread(image_path)
    boxes, weights = hog.detectMultiScale(img, winStride=(4, 4))
    return len(boxes)


class PeopleCounter1(MethodView):
    def get(self):
        try:
            file_path = 'images/droga.jpg'
            people = count_people(file_path)
            return jsonify({"Number of people": people})
        except Exception as e:
            return jsonify({"error": str(e)})


class PeopleCounter2(MethodView):
    def get(self):
        try:
            img_url = request.args.get('img_url')
            # http://127.0.0.1:5000/2/?img_url=adres_zdjecia
            resp = urlopen(img_url)
            img2 = np.asarray(bytearray(resp.read()), dtype="uint8")
            img2 = cv2.imdecode(img2, cv2.IMREAD_COLOR)
            boxes, weights = hog.detectMultiScale(img2, winStride=(4, 4))
            return {'count': len(boxes)}
        except Exception as e:
            return jsonify({"error": str(e)})


class PeopleCounter3(Resource):
    def post(self):
        if 'file' not in request.files:
            return jsonify({"error": "No file part"})

        file = request.files['file']

        if file.filename == '':
            return jsonify({"error": "No selected file"})

        if file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                # Save the uploaded file
                upload_folder = 'uploads'
                os.makedirs(upload_folder, exist_ok=True)
                file_path = os.path.join(upload_folder, file.filename)
                file.save(file_path)

                # Count people in the image
                people = count_people(file_path)

                # Remove the uploaded file after processing
                os.remove(file_path)

                return jsonify({"Number of people": people})
            except Exception as e:
                return jsonify({"error": str(e)})
        else:
            return jsonify({"error": "wrong extension"})
