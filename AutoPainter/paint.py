from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import base64

import json
import tensorflow as tf
from pylab import *
import os
import cv2

UPLOAD_FOLDER = './AutoPainter/media/before_image'
RESULT_FOLDER = './AutoPainter/media/after_image'
ALLOWED_IMAGE_EXTENSIONS = set(['png', 'bmp', 'jpg', 'jpeg'])

os.environ["CUDA_VISIBLE_DEVICES"] = "1"
model = {}

def allowed_file(filename):
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1] in ALLOWED_IMAGE_EXTENSIONS
    )
    
def load_model(local_models_dir):
    for name in os.listdir(local_models_dir):
        if name.startswith("."):
            continue

        with tf.compat.v1.Graph().as_default() as graph:
            config = tf.compat.v1.ConfigProto()
            config.gpu_options.allow_growth = True
            sess = tf.compat.v1.Session(config=config,graph=graph)
            saver = tf.compat.v1.train.import_meta_graph(os.path.join(local_models_dir, "export.meta"))

            saver.restore(sess, os.path.join(local_models_dir, "export"))
            input_vars = json.loads(tf.compat.v1.get_collection("inputs")[0].decode("utf-8"))
            output_vars = json.loads(tf.compat.v1.get_collection("outputs")[0].decode("utf-8"))
            input = graph.get_tensor_by_name(input_vars["input"])
            output = graph.get_tensor_by_name(output_vars["output"])

            if name not in model:
                model[name] = {}

            model[name]["local"] = dict(
                sess=sess,
                input=input,
                output=output,
            )

def input_pic(input_dir, output_dir):
    f = open(str(input_dir), 'rb')
    filedata = f.read()
    f.close()
    filedata = bytearray(filedata)
    input_b64data = base64.urlsafe_b64encode(filedata)
    m = model["checkpoint"]["local"]
    output_b64data = m["sess"].run(m["output"], feed_dict={m["input"]: [input_b64data]})[0]
    output_b64data += b'=' * (-len(output_b64data) % 4)
    output_data = base64.urlsafe_b64decode(output_b64data)
    f2 = open(output_dir, 'wb')
    f2.write(output_data)
    f2.close()

def paint(image, model_path):
    load_model(model_path)
    proceccing(image)
    
    before_image = './AutoPainter/media/before_image/' + str(image)[str(image).index('/')+1:]
    after_image = './AutoPainter/media/after_image/' + str(image)[str(image).index('/')+1:]
    
    input_pic(before_image, after_image)

def proceccing(image):
        im = cv2.imread('./AutoPainter/media/'+str(image))
        im = cv2.resize(im, [512,512])
        cv2.imwrite('./AutoPainter/media/'+str(image), im)
