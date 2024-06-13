from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dash_app import dash_app  # Import the Dash app
import logging
from model_utils import predict  # Import the new functions
import numpy as np
import warnings
import os

# Disable oneDNN custom operations warning
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Suppress TensorFlow CPU optimization warnings
warnings.filterwarnings("ignore", message=".*oneDNN custom operations are on.*")
warnings.filterwarnings("ignore", message=".*This TensorFlow binary is optimized.*")

flask_app = Flask(__name__)
flask_app.secret_key = os.getenv("SECRET_KEY", "default_secret_key")

@flask_app.route('/')
def index():
    # Check if dark mode preference is stored in session
    dark_mode = session.get('dark_mode', False)
    return render_template('index.html', dark_mode=dark_mode)

@flask_app.route('/toggle_dark_mode')
def toggle_dark_mode():
    # Toggle dark mode preference in session
    session['dark_mode'] = not session.get('dark_mode', False)
    return redirect(request.referrer or url_for('index'))

# Define a function to interpret the prediction
def interpret_prediction(prediction):
    if prediction >= 0.5:
        return 'Likely Diabetic'
    else:
        return 'Non-Diabetic'

# Define a route for prediction
@flask_app.route('/predict', methods=['POST'])
def predict_route():
    try:
        input_data = request.form.to_dict()
        prediction_prob = predict(input_data)
        diagnosis = interpret_prediction(prediction_prob)
        return jsonify({'diagnosis': diagnosis})
    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

# Set the server attribute of Dash app to the Flask app
dash_app.init_app(flask_app)
dash_app.url_base_pathname = '/visualisation'

if __name__ == '__main__':
    flask_app.run()

