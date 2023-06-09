#!/usr/bin/env python

import io
import json

from flask import request, send_from_directory, Flask
#from keras.models import load_model
import pandas as pd
import pickle

#from project import encode_data


attack = {"normal" : 0, "dos" : 1, "probe" : 2, "r2l" : 3, "u2r" : 4}


os_table = {
            0  : "Linux (kernel 2.4 and 2.6)",
            1 : "Linux",
            2  : "Google's customized Linux",
            3 : "FreeBSD or Mac OS",
            4: "Windows XP or Windows 10",
            5 : "Windows 7, Vista and Server 2008",
            6: "Windows 10",
            7 : "Cisco Router (IOS 12.4)"
        }
def attack_map(attack_type):
    return os_table[attack[attack_type]]

with open('encoding.json') as f:
    encodings = json.load(f)
    encodings[1] = encodings['1']
    encodings[2] = encodings['2']
    encodings[3] = encodings['3']
    encodings[41] = encodings['41']

#model = load_model('keras.model')
model = pickle.load(open("DT_model.pkl","rb"))
app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('', 'index.html')


@app.route('/test_packet', methods=['POST'])
def test_packet():
    """
    Example input that browser UI should provide:

    normal.
    0,tcp,http,SF,181,5450,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,8,8,0.00,0.00,0.00,0.00,1.00,0.00,0.00,9,9,1.00,0.00,0.11,0.00,0.00,0.00,0.00,0.00

    smurf.
    0,icmp,ecr_i,SF,1032,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,107,107,0.00,0.00,0.00,0.00,1.00,0.00,0.00,255,107,0.42,0.02,0.42,0.00,0.00,0.00,0.00,0.00
    """
    data = request.form['packet'].encode('utf8')
    data = pd.read_csv(io.BytesIO(data), header=None)
    print("CSV ", data)
    encode_data(data, cols=(1, 2, 3), encodings=encodings)
    print("Successful encoded data ", data)
    #prediction = model.predict_classes(data)
    prediction = model.predict(data)
    print("Prediction: ", prediction)
    response_data = {"class": prediction[0]+',Client OS predicted:'+attack_map(prediction[0])}  # We are only sending one packet at a time from the UI
    response = app.response_class(response=json.dumps(response_data),
                                  status=200,
                                  mimetype='application/json')
    return response


app.run(host='0.0.0.0')
