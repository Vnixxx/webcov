import os
import uuid
import flask
import urllib
import numpy as np
import cv2
import tensorflow as tf
from PIL import Image
from tensorflow.keras.models import load_model
from flask import Flask , render_template  , request , send_file
from tensorflow.keras.preprocessing.image import load_img , img_to_array
import matplotlib.pyplot as plt
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = load_model(os.path.join(BASE_DIR , 'covidl.h5'))
ALLOWED_EXT = set(['jpg' , 'jpeg' , 'png' , 'jfif'])
def allowed_file(filename):
    
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT
classes =  ['Atelectasis',
 'Cardiomegaly',
 'Consolidation',
 'Edema',
 'Effusion',
 'Emphysema',
 'Fibrosis',
 'Infiltration',
 'Mass',
 'Nodule',
 'Pleural_Thickening',
 'Pneumonia',
 'Pneumothorax']
def predict(filename , model):
    # NoneType = type(None)
    # an_image = plt.imread(filename)
    # rgb_weights = [0.2989, 0.5870, 0.1140]
    # img = np.dot(an_image[..., :3], rgb_weights)
    # img = load_img(filename , target_size = (128 , 128))
    # img = img_to_array(img)
    # img = img.reshape(NoneType, 128 ,128,1)
    # img = img.astype('float32')
    # img = img/255.0
    img = cv2.imread(filename)
    img = cv2.resize(img,(128,128),interpolation = cv2.INTER_AREA)
    # img = img.resize(img,(128,128))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = img.reshape(1,128,128,1)
    # img = tf.expand_dims(img, axis=0)
    # if img.mode=='RGB':
    #     return render_template("about.html")
    # img = img.reshape(1)
    # image = img[np.newaxis, ...]
    # image = image / 255.
    result = model.predict(img)
    dict_result = {}
    for i in range(13):
        dict_result[result[0][i]] = classes[i]
    res = result[0]
    res.sort()
    res = res[::-1]
    prob = res[:3]
    
    prob_result = []
    class_result = []
    for i in range(3):
        prob_result.append((prob[i]*100).round(2))
        class_result.append(dict_result[prob[i]])
    return class_result , prob_result
@app.route('/')
def home():
        return render_template("inno.html")
@app.route('/inno')
def inno():
        return render_template("inno.html")
@app.route('/success' , methods = ['GET' , 'POST'])
def success():
    error = ''
    target_img = os.path.join(os.getcwd() , 'static/images') 
    if request.method == 'POST':
        if(request.form):
            link = request.form.get('link')
            try :
                resource = urllib.request.urlopen(link)
                unique_filename = str(uuid.uuid4())
                filename = unique_filename+".jpg"
                img_path = os.path.join(target_img , filename)
                output = open(img_path , "wb")
                output.write(resource.read())
                output.close()
                img = filename
                class_result , prob_result = predict(img_path , model)
                predictions = {
                      "class1":class_result[0],
                        "class2":class_result[1],
                        "class3":class_result[2],
                        "prob1": prob_result[0],
                        "prob2": prob_result[1],
                        "prob3": prob_result[2],
                }
            except Exception as e : 
                print(str(e))
                error = 'This image from this site is not accesible or inappropriate input'
            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                return render_template('inno.html' , error = error) 
            
        elif (request.files):
            file = request.files['file']
            if file and allowed_file(file.filename):
                file.save(os.path.join(target_img , file.filename))
                img_path = os.path.join(target_img , file.filename)
                img = file.filename
                class_result , prob_result = predict(img_path , model)
                predictions = {
                      "class1":class_result[0],
                        "class2":class_result[1],
                        "class3":class_result[2],
                        "prob1": prob_result[0],
                        "prob2": prob_result[1],
                        "prob3": prob_result[2],
                }
            else:
                error = "Please upload images of jpg , jpeg and png extension only"
            if(len(error) == 0):
                return  render_template('success.html' , img  = img , predictions = predictions)
            else:
                return render_template('inno.html' , error = error)
    else:
        return render_template('inno.html')
@app.route('/about' , methods = ['GET','POST'])
def about():
    # if request.method == 'POST':
    #     return 
    return render_template("about.html")
@app.route('/howto' , methods = ['GET','POST'])
def howto():
    return render_template("howto.html")
@app.route('/research' , methods = ['GET','POST'])
def research():
    return render_template("research.html")
if __name__ == "__main__":
    app.run(debug = True)