from flask import Flask, request, jsonify
import joblib
import numpy as np
from tensorflow.keras.models import load_model
import pandas as pd


app = Flask(__name__)
model = load_model('lamp_status_model.h5')
le = joblib.load('label_encoder.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)

    room = data['room']
    time = data['time']

    df = pd.DataFrame([{'room': room, 'time': time}]).values

    df = pd.DataFrame([{'room': room, 'time': time}])

    le = joblib.load('label_encoder.pkl')

    df['room'] = le.fit_transform(df['room'])

    df = df.values

    input_data = df.reshape((df.shape[0], 1, df.shape[1]))
    prediction = model.predict(input_data)
    print(prediction)
    prediction = 'on' if prediction[0][0] > 0.5 else 'off'

    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(port=5000)
 