from flask import Flask, render_template, request, jsonify
import numpy as np
import pickle
import json
import os

# Initialize Flask app
app = Flask(__name__)

# Load the model (make sure the path is correct)
model_path = 'C:/bangalore_home_price_predictor/backend/banglore_home_prices_model.pickle'
with open(model_path, 'rb') as f:
    model = pickle.load(f)

# Load the locations from the JSON file (make sure the path is correct)
locations_path = 'C:/bangalore_home_price_predictor/backend/artifacts/columns.json'
with open(locations_path, 'r') as f:
    columns_data = json.load(f)

# Extract the location names (skip the first three columns which are not locations)
location_names = columns_data["data_columns"][3:]

# Route for the homepage
@app.route('/')
def home():
    # Pass the location names list to the template
    return render_template('index.html', locations=location_names)



# Route to get the predicted price
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the request
        data = request.get_json()

        # Extract features from the POST request in order: location, area, bhk, bath
        area = data['area']
        bhk = data['bhk']
        bath = data['bath']
        location = data['location']

        # Convert location to index using the loaded locations
        try:
            location_index = columns_data["data_columns"].index(location)
        except ValueError:
            location_index = -1  # If location is not found in the list

        # Log the location index and the extracted data
        print(f"Location: {location}, Location Index: {location_index}")
        print(f"Area: {area}, BHK: {bhk}, Bath: {bath}")

        # If the location is not found in the model data
        if location_index == -1:
            return jsonify({'error': 'Location not found in the model data.'})

        # Create input features array (order: location, area, bhk, bath)
        input_features = np.zeros(len(columns_data["data_columns"]))  # initialize all as 0
        input_features[0] = area  # Assign area value
        input_features[1] = bhk   # Assign bhk value
        input_features[2] = bath  # Assign bath value
        input_features[location_index] = 1  # Set the corresponding location column to 1

        # Log the input features to verify
        print(f"Input Features: {input_features}")

        # Make prediction using the loaded model
        predicted_price = model.predict(input_features.reshape(1, -1))

        # Log the predicted price (already in Lakhs)
        print(f"Predicted Price in Lakhs: {predicted_price[0]}")

        # Round to 2 decimal places
        formatted_price = round(predicted_price[0], 2)

        # Log the formatted price
        print(f"Formatted Predicted Price: {formatted_price} Lakhs")

        # Return the formatted predicted price in Lakhs
        return jsonify({'predicted_price': f'{formatted_price} Lakhs'})

    except Exception as e:
        return jsonify({'error': str(e)})




# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

