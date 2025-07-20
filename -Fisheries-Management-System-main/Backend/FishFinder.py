from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import requests
import random

app = Flask(__name__)
CORS(app)

# Load your ML model for fish presence
model = joblib.load('fish_predictor_model.pkl')

# Example: serve Goa ocean data
@app.route('/data', methods=['GET'])
def get_data():
    df = pd.read_csv('goa_daily_salinity.csv')
    return jsonify(df.to_dict(orient='records'))

# ML prediction endpoint (existing)
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        salinity = float(data['salinity'])
        temperature = float(data['temperature'])

        prediction = model.predict([[salinity, temperature]])
        return jsonify({'fish_present': int(prediction[0])})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# New: Find Fish endpoint (migration zones based on temperature and month)
@app.route('/find_fish', methods=['POST'])
def find_fish():
    try:
        data = request.get_json()
        month = int(data['month'])  # No longer using user-provided temperature
        current = random.uniform(-1, 1)
        chlorophyll = random.uniform(0.1, 0.5)

        # OpenWeather API configuration (replace with your API key)
        API_KEY = "your_openweather_api_key_here"  # Sign up at openweathermap.org to get this
        BASE_URL = "https://api.openweathermap.org/data/3.0/onecall"

        # Coordinates for Goa zones (approximate)
        ZONE_COORDS = {
            "Calangute": {"lat": 15.5436, "lon": 73.7571},
            "Baga": {"lat": 15.5500, "lon": 73.7500},
            "Colva": {"lat": 15.2777, "lon": 73.9214}
        }

        # Fetch temperature for a random zone
        zone = random.choice(list(ZONE_COORDS.keys()))
        lat, lon = ZONE_COORDS[zone]["lat"], ZONE_COORDS[zone]["lon"]
        params = {
            "lat": lat,
            "lon": lon,
            "appid": API_KEY,
            "units": "metric"  # Temperature in Celsius
        }
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            temperature = data["current"]["temp"]  # Current temperature in °C
        except Exception as e:
            print(f"Error fetching temperature: {e}")
            temperature = 28.0  # Fallback to default value if API fails

        # Synthetic model for zone prediction (unchanged except temperature input)
        zones = ["Calangute", "Baga", "Colva"]
        species = ["Sardine", "Mackerel", "Tuna"]
        synthetic_data = []
        for _ in range(150):
            m = random.randint(1, 12)
            t = random.uniform(26, 32)  # This is now overridden by OpenWeather data
            c = random.uniform(-1, 1)
            ch = random.uniform(0.1, 0.5)
            s = random.choice(species)
            if t > 29 and m in [10, 11, 12] and c > 0:
                z = "Calangute"
            elif t < 28 and c < 0:
                z = "Colva"
            else:
                z = "Baga"
            synthetic_data.append([t, m, c, ch, z, s])
        
        X = np.array([[d[0], d[1], d[2], d[3]] for d in synthetic_data])
        y = np.array([d[4] for d in synthetic_data])
        zone_model = DecisionTreeClassifier()
        zone_model.fit(X, y)

        # Use fetched temperature for prediction
        prediction = zone_model.predict([[temperature, month, current, chlorophyll]])
        predicted_zone = prediction[0]
        species_pred = random.choice(species)
        
        score = min(100, int(chlorophyll * 200))
        tip = (
            "Limit catch to 500 kg to preserve stocks." if score < 50 else
            "Sustainable fishing OK—target 750 kg max." if score < 75 else
            "High abundance—fish freely, max 1000 kg."
        )
        color = "red" if score < 50 else "yellow" if score < 75 else "green"

        return jsonify({
            'zone': predicted_zone,
            'species': species_pred,
            'sst': round(temperature, 1),  # Updated with real temperature
            'current': round(current, 2),
            'chlorophyll': round(chlorophyll, 2),
            'score': score,
            'tip': tip,
            'color': color
        })
    except Exception as e:
        return jsonify({'zone': 'Error', 'tip': f'Failed to find fish. {str(e)}'}), 400

# Serve historical migration data from CSV
@app.route('/historical_migration', methods=['GET'])
def get_historical_migration():
    try:
        df = pd.read_csv('historical_migration_data.csv')
        return jsonify(df.to_dict(orient='records'))
    except Exception as e:
        return jsonify({'error': f'Failed to load historical data: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)