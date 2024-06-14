# nhanesDM https://nhanesdm-5a06a4078888.herokuapp.com/

### The dataset, sourced from National Health and Nutrition Examination Survey (NHANES) for educational purposes, is used to develop a website that facilitates machine learning predictions for diabetes and features an interactive dashboard.

## Key Components:

### Flask Application (app.py):
- Manages routes for rendering templates and handling predictions.
- Provides routes for toggling dark mode and serving the Dash app.

### Dash Application (dash_app.py):
- Implements interactive data visualizations with filters for diabetes data.
- Uses Bootstrap for theming and styling.
- Contains a clientside callback to handle theme switching.

### Model Utilities (model_utils.py):
- Handles loading of the trained model, scaler, and encoder.
- Provides preprocessing and prediction functions for the model.

### Data Preprocessing (dataCleaning.ipynb)
- Data Loading:
  - Load the dataset using pd.read_csv().
  - Display the first few rows to understand the structure of the data.

- Data Preprocessing:
  - Handle missing values by filling them with the mean of each column.
  - Separate features and target variable.
  - Encode categorical features using OneHotEncoder.
  - Scale numerical features using StandardScaler.

- Model Training:

  - Split the data into training and testing sets.
  - Train a Random Forest model and neural network using Keras.

- Model Evaluation:
  - Evaluate the performance of each model using classification reports.
    
- Model Saving:
  - Save the trained models, scaler, and encoder using joblib.
  - Save the neural network model using Keras' model.save() function.
