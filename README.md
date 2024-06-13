# nhanesDM

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
-- Load the dataset using pd.read_csv().
-- Display the first few rows to understand the structure of the data.

- Data Preprocessing:

Handle missing values by filling them with the mean of each column.
Separate features and target variable.
Encode categorical features using OneHotEncoder.
Scale numerical features using StandardScaler.
Feature Engineering:

Combine scaled numerical and encoded categorical features into a single feature matrix X.
Model Training:

Split the data into training and testing sets.
Train a Logistic Regression model and a Random Forest model.
Train a neural network using Keras.
Model Evaluation:

Evaluate the performance of each model using classification reports.
Model Saving:

Save the trained models, scaler, and encoder using joblib.
Save the neural network model using Keras' model.save() function.
