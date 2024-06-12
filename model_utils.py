import logging
import pandas as pd
import joblib

model = None
scaler = None
encoder = None

def get_model_scaler_and_encoder():
    global model, scaler, encoder
    if model is None:
        try:
            model = joblib.load('your_trained_model.pkl') 
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            raise
    if scaler is None:
        try:
            scaler = joblib.load('your_scaler.pkl')        
        except Exception as e:
            logging.error(f"Error loading scaler: {e}")
            raise
    if encoder is None:
        try:
            encoder = joblib.load('your_encoder.pkl')    
        except Exception as e:
            logging.error(f"Error loading encoder: {e}")
            raise
    return model, scaler, encoder

def preprocess_input(data):
    input_features = [
        'age', 'race', 'gender', 'maritalStatus', 'householdSize',
        'bpSys', 'cholesterol', 'glucose_level', 'bmi', 'arthritis',
        'heartAttack', 'stroke', 'hypertension', 'walkDiff',
        'interestInDoingThings', 'tiredOrLowEnergy', 'depressedOrHopeless',
        'troubleSleeping'
    ]

    input_df = pd.DataFrame([data])
    input_df = input_df[input_features]
    
    model, scaler, encoder = get_model_scaler_and_encoder()
    try:
        # Encode categorical features
        columns_to_transform = ['race', 'maritalStatus']
        df_selected = input_df[columns_to_transform]
        transformed_data = encoder.transform(df_selected)
        feature_names = encoder.get_feature_names_out(columns_to_transform)
        transformed_df = pd.DataFrame(transformed_data, columns=feature_names)
        input_df.drop(columns=columns_to_transform, inplace=True)
        df_ml_transformed = pd.concat([input_df, transformed_df], axis=1)
        scaled_values = scaler.transform(df_ml_transformed)  
    except Exception as e:
        logging.error(f"Error preprocessing input: {e}")
        raise
    return scaled_values

def predict(data):
    scaled_input = preprocess_input(data)
    model, scaler, _ = get_model_scaler_and_encoder()
    try:
        prediction = model.predict(scaled_input)[0]
    except Exception as e:
        logging.error(f"Error predicting: {e}")
        raise
    return prediction
