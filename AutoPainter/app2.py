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
from .demo_new import *

UPLOAD_FOLDER = './AutoPainter/media/before_image'
RESULT_FOLDER = './AutoPainter/media/after_image'
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpeg'])

def trans1(imf):
    try:
        filename_ = str(time.time()).replace('.', '_') + '.png'
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        filename2 = os.path.join(RESULT_FOLDER, filename_)
        imf = base64.b64decode(imf)
        with open(filename, "wb") as f:
            f.write(imf)
        im = io.imread(filename)
        im = transform.resize(im, [512,512])
        io.imsave(filename, im)
        input_pic1(filename, filename2)

    except Exception as err:
        return err
    return filename


def trans2(imf):
    try:
        filename_ = str(time.time()).replace('.', '_') + '.png'
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        filename2 = os.path.join(RESULT_FOLDER, filename_)
        imf = base64.b64decode(imf)
        with open(filename, "wb") as f:
            f.write(imf)
        im = io.imread(filename)
        im = transform.resize(im, [512,512])
        io.imsave(filename, im)
        input_pic2(filename, filename2)

    except Exception as err:
        return err
    return filename

def sketchify2(imf):
    try:
        filename_ = str(time.time()).replace('.', '_') + '.png'
        filename = os.path.join(UPLOAD_FOLDER, filename_)
        filename2 = os.path.join(RESULT_FOLDER, filename_)
        imf = base64.b64decode(imf)
        with open(filename, "wb") as f:
            f.write(imf)
        im = io.imread(filename)
        im = transform.resize(im, [512,512])
        io.imsave(filename, im)
        sketchify(filename, filename2)

    except Exception as err:
        return err
    return filename