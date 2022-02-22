import os
import uuid

from flask import Flask, request, json, jsonify
from keras.models import load_model

from method import Model
app = Flask(__name__)
UPLOAD_FOLDER = './Imgs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model = Model( 7 ,  224 ,0.0001 , "../Models/s_19.h5")
data={}
data = json.load(open('../Labels/s_19.json'))

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        path = request.form.get('imgPath')
        resultFromModel =model.simulation(path)
        resultList =[]
        for result in resultFromModel:
            resultList.append({'diseases' : data[str(result.index)] , 'probability' :result.prop })
        return jsonify(data= resultList)
    else:
        return jsonify(data=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0' , port=5020 , debug =False )