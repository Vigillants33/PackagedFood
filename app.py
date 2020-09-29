# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 20:35:18 2020

@author: Rohini
"""


from __future__ import division, print_function
import sys
import os
import numpy as np

from flask import Flask, redirect, url_for, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer

import pytesseract
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = ‘/app/.apt/usr/bin/tesseract’

# Define a flask app
app = Flask(__name__)


def model_predict(path):
    
    
    black = (0,0,0)
    white = (255,255,255)
    threshold = (160,160,160)
    img = Image.open(path).convert("LA")
    pixels = img.getdata()
    newPixels = []
    allergen = ["Spelt","Rye","Nuts","Barley","Oats","Milk","Eggs","Fish","Crustacean shellfish","Tree nuts","Peanuts","Wheat","Bass","Flounder","Clam","Crab","Shrimp","Lobster","Walnut","Pecan","Cocoa","Soy","Sesame","Corn","Palm Oil","Coconut Oil","Almonds","Mustard","Sunflower","Glucose","Honey","Quinoa","Rosemary","Celery","Yeast","Cereals","Pork","Chicken","Sulphites","Hazelnuts","Vanilla","Butter","Mixed Fruit","Seeds","Pistachios"] 
    for pixel in pixels:
        if pixel < threshold:
            newPixels.append(black)
        else:
            newPixels.append(white)
    newImg = Image.new("RGB",img.size)
    newImg.putdata(newPixels)
    text = pytesseract.image_to_string(newImg)
    final=""
    for ele in text:
        if(ele.isalpha()):
            final+=ele.upper()
        elif(ele=="\n"):
            continue
        else:
            final+=ele
    present=[]
    for ele in allergen:
        ele=ele.upper()
        if(ele in final or ele[1:] in final or ele[:-1] in final):
            present.append(ele)
    r=",".join(present)
    return ("ALLERGIES : "+r)
    

@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
   
        file_path = os.path.join('uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path)

        return preds
    return None


if __name__ == '__main__':
    app.run(debug=False)

