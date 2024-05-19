import numpy as np
import pickle
from flask import Flask, request, render_template

app = Flask(__name__)

# Function to load models safely
def load_model(path):
    with open(path, 'rb') as file:
        return pickle.load(file)

# Load machine learning models using a function to handle file operations safely
model_sf = load_model('.//code//model//models//sf_RFR_final_model.pkl')
model_mv = load_model('.//code//model//models//mv_RFR_final_model.pkl')
model_sj = load_model('.//code//model//models//sj_RFR_final_model.pkl')
model_re = load_model('.//code//model//models//re_RFR_final_model.pkl')
model_pa = load_model('.//code//model//models//pa_RFR_final_model.pkl')

@app.route('/')
def home():
    return render_template('app_new.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Ensure there is input data from the form
        if not request.form.values():
            return render_template('app_new.html', result="No input data provided.")

        # Extract features and city index from form
        features = [float(x) for x in request.form.values()]
        if not features:
            return render_template('app_new.html', result="No numerical input provided.")

        city_index = int(features.pop(0))  # Assume first entry is city index, pop it out

        # Validate city index
        models = [model_sf, model_sj, model_re, model_mv, model_pa]
        if city_index < 0 or city_index >= len(models):
            return render_template('app_new.html', result=f"City index {city_index} is out of range.")

        model = models[city_index]

        # Predict using the correct model
        prediction = model.predict([features])[0]

        # Render result
        return render_template('app_new.html', result=prediction)

    except ValueError as ve:
        return render_template('app_new.html', result=str(ve))
    except Exception as e:
        return render_template('app_new.html', result=f"Error processing request: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)  # Remember to turn off debug mode in production