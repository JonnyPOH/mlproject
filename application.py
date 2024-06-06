from flask import Flask, request, render_template
import numpy as np
import pandas as pd
import logging
from sklearn.preprocessing import StandardScaler
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from flask_socketio import SocketIO, emit

application = Flask(__name__)
app = application
socketio = SocketIO(app)

logging.basicConfig(level=logging.INFO)

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predictdata', methods=['GET', 'POST'])
def predict_datapoint():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('writing_score')),
            writing_score=float(request.form.get('reading_score'))
        )

        app.logger.info("Received data: %s", data)
        socketio.emit('log', {'message': f"Received data: {data}"})

        pred_df = data.get_data_as_data_frame()
        app.logger.info("Data as DataFrame: %s", pred_df)
        socketio.emit('log', {'message': f"Data as DataFrame: {pred_df}"})

        predict_pipeline = PredictPipeline()
        app.logger.info("Predict Pipeline created: %s", predict_pipeline)

        results = predict_pipeline.predict(pred_df)
        app.logger.info("Prediction results: %s", results)
        socketio.emit('log', {'message': f"Prediction results: {results}"})

        return render_template('home.html', results=results[0])

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0")
