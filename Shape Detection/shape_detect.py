import os
from uuid import uuid4
import cv2
import numpy as np
font = cv2.FONT_HERSHEY_COMPLEX

from flask import Flask, request, render_template, send_from_directory

__author__ = 'salman_faroz'

app = Flask(__name__)



APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, 'images/')
    print(target)
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        destination = "/".join([target, filename])
        print ("Accept incoming file:", filename)
        print ("Save it to:", destination)
        upload.save(destination)
    to="./images/"+filename
    img = cv2.imread(to)
    imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray,127,255,0)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
    	approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    if len(approx) == 4:
    	(x, y, w, h) = cv2.boundingRect(approx)
    	ar = w / float(h)
    	shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
    	return "<center><h1>square</h1></center>"

    elif len(approx) == 3:
        return "<center><h1>Triangle</h1></center>"

    elif len(approx) == 5:
        return "<center><h1>Pentagon</h1></center>"

    elif 6 < len(approx) < 15:
        return "<center><h1>Ellipse</h1></center>"

    else:
        return "<center><h1>Circle</h1></center>"


@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

if __name__ == "__main__":
    app.run(port=4555, debug=True)
