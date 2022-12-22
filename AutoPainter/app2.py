import os
import time
import datetime
import logging
import flask
import werkzeug
import tornado.wsgi
import tornado.httpserver
import numpy as np
from PIL import Image
import urllib
import cv2

from skimage import io, transform, exposure
from demo_new import *

UPLOAD_FOLDER = './AutoPainter/media/before_image'
RESULT_FOLDER = './AutoPainter/media/after_image'
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpeg'])

def trans1(imf):
    try:
        imf = cv2.imread('./AutoPainter/media/'+str(imf))
        filename_ = str(time.time()).replace('.', '_') + '.png'
#        filename_ = 'tmp.jpg'
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        filename2 = os.path.join(RESULT_FOLDER, filename_)
        imf = base64.b64decode(imf)
        with open(filename, "wb") as f:
            f.write(imf)
        im = io.imread(filename)
        im = transform.resize(im, [512,512])
        io.imsave(filename, im)
        logging.info('Saving to %s.', filename)
        input_pic(filename, filename2)

    except Exception as err:
        logging.info('Uploaded image open error: %s', err)

    return json.dumps({"image2":filename2})

def trans2():
    try:
        # We will save the file to disk for possible data collection.
        imf = flask.request.form['image']
        filename_ = str(time.time()).replace('.', '_') + '.png'
#        filename_ = 'tmp.jpg'
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        filename2 = os.path.join(RESULT_FOLDER, filename_)
        imf = base64.b64decode(imf)
        with open(filename, "wb") as f:
            f.write(imf)
        im = io.imread(filename)
        im = transform.resize(im, [512,512])
        io.imsave(filename, im)
        logging.info('Saving to %s.', filename)
        input_pic2(filename, filename2)

    except Exception as err:
        logging.info('Uploaded image open error: %s', err)
        return flask.render_template(
            'index3.html', has_result=True,
            result=(False, 'Cannot open uploaded image.')
        )

    return json.dumps({"image2":filename2})

def trans3():
    try:
        # We will save the file to disk for possible data collection.
        imf = flask.request.form['image']
        filename_ = str(time.time()).replace('.', '_') + '.png'
#        filename_ = 'tmp.jpg'
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        filename2 = os.path.join(RESULT_FOLDER, filename_)
        imf = base64.b64decode(imf)
        with open(filename, "wb") as f:
            f.write(imf)
        im = io.imread(filename)
        im = transform.resize(im, [512,512])
        io.imsave(filename, im)
        logging.info('Saving to %s.', filename)
        input_pic3(filename, filename2)

    except Exception as err:
        logging.info('Uploaded image open error: %s', err)
        return flask.render_template(
            'index3.html', has_result=True,
            result=(False, 'Cannot open uploaded image.')
        )

    return json.dumps({"image2":filename2})
 

def sketchify2():
    try:
        # We will save the file to disk for possible data collection.
        imf = flask.request.form['image']
        filename_ = str(time.time()).replace('.', '_') + '.png'
#        filename_ = 'tmp.jpg'
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        filename2 = os.path.join(RESULT_FOLDER, filename_)
        imf = base64.b64decode(imf)
        with open(filename, "wb") as f:
            f.write(imf)
        im = io.imread(filename)
        im = transform.resize(im, [512,512])
        io.imsave(filename, im)
        logging.info('Saving to %s.', filename)
        sketchify(filename, filename2)

    except Exception as err:
        logging.info('Uploaded image open error: %s', err)
        return flask.render_template(
            'index3.html', has_result=True,
            result=(False, 'Cannot open uploaded image.')
        )

    return json.dumps({"image1":filename2})

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS
    )


