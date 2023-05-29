#!/usr/bin/env python

import io
import json

from flask import request, send_from_directory, Flask
#from keras.models import load_model
import pandas as pd
import pickle

#from project import encode_data


attack = {0:"Level 1", 1:"Level 2",2:"level 3"}




#model = load_model('keras.model')
model = pickle.load(open("model.pkl","rb"))
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('', 'index.html')


@app.route('/test_packet', methods=['POST'])
def test_packet():
    """
    Example input that browser UI should provide:

    Level 3.
    6854,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,9,3,1,3,31,0,0,2,2,0.93441081,9,2,13,7,12,-8.95,51.9,7

    Level 1
    68764,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,3,0,3,31,0,0,0,0,0.956976175,6,2,13,7,12,-8.95,51.9,7

    

    
    Level 1
    4030,2,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,8,0,31,0,0,1,1.270368099,0,2,21,53,52,30.2642,59.8944,53
    """
    
    data = request.form['packet'].encode('utf8')
    data = pd.read_csv(io.BytesIO(data), header=None)
    print("CSV ", data)
    #encode_data(data, cols=(1, 2, 3), encodings=encodings)
    print("Successful encoded data ", data)
    #prediction = model.predict_classes(data)
    prediction = model.predict(data)
    print("Prediction: ", prediction)
    response_data = {"class": attack[prediction[0]]}  # We are only sending one packet at a time from the UI
    response = app.response_class(response=json.dumps(response_data),
                                  status=200,
                                  mimetype='application/json')
    return response


app.run(host='0.0.0.0')
