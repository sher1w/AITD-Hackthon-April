from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import requests
import numpy as np
from sklearn.tree import DecisionTreeClassifier
import random
from datetime import datetime, timedelta

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

# Existing: Find Fish endpoint (migration zones)
@app.route('/find_fish', methods=['POST'])
def find_fish():
    try:
        data = request.get_json()
        temperature = float(data['temperature'])
        month = int(data['month'])
        current = random.uniform(-1, 1)
        chlorophyll = random.uniform(0.1, 0.5)

        zones = ["Calangute", "Baga", "Colva"]
        synthetic_data = []
        for _ in range(150):
            m = random.randint(1, 12)
            t = random.uniform(26, 32)
            c = random.uniform(-1, 1)
            ch = random.uniform(0.1, 0.5)
            if t > 29 and m in [10, 11, 12] and c > 0:
                z = "Calangute"
            elif t < 28 and c < 0:
                z = "Colva"
            else:
                z = "Baga"
            synthetic_data.append([t, m, c, ch, z])
        
        X = np.array([[d[0], d[1], d[2], d[3]] for d in synthetic_data])
        y = np.array([d[4] for d in synthetic_data])
        zone_model = DecisionTreeClassifier()
        zone_model.fit(X, y)

        prediction = zone_model.predict([[temperature, month, current, chlorophyll]])
        zone = prediction[0]
        
        score = min(100, int(chlorophyll * 200))
        tip = (
            "Limit catch to 500 kg to preserve stocks." if score < 50 else
            "Sustainable fishing OK—target 750 kg max." if score < 75 else
            "High abundance—fish freely, max 1000 kg."
        )
        color = "red" if score < 50 else "yellow" if score < 75 else "green"

        return jsonify({
            'zone': zone,
            'sst': round(temperature, 1),
            'current': round(current, 2),
            'chlorophyll': round(chlorophyll, 2),
            'score': score,
            'tip': tip,
            'color': color
        })
    except Exception as e:
        return jsonify({'zone': 'Error', 'tip': f'Failed to find fish. {str(e)}'}), 400

# Existing: Get temperature from Open-Meteo API
@app.route('/get_temperature', methods=['GET'])
def get_temperature():
    try:
        lat = request.args.get('lat', default=15.2993, type=float)
        lon = request.args.get('lon', default=74.1240, type=float)

        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}¤t_weather=true"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200 and 'current_weather' in data:
            temperature_c = data['current_weather']['temperature']
            return jsonify({'temperature': temperature_c, 'unit': data['current_weather']['temperature_unit']})
        else:
            return jsonify({'error': 'Failed to fetch temperature data'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# New: Historical migration patterns
@app.route('/historical_migration', methods=['GET'])
def historical_migration():
    try:
        # Simulate 5 years of data (2020-2024)
        years = range(2020, 2025)
        historical_data = []
        for year in years:
            for month in range(1, 13):
                temp = random.uniform(26, 32)
                current = random.uniform(-1, 1)
                chlorophyll = random.uniform(0.1, 0.5)
                if temp > 29 and month in [10, 11, 12] and current > 0:
                    zone = "Calangute"
                elif temp < 28 and current < 0:
                    zone = "Colva"
                else:
                    zone = "Baga"
                historical_data.append({
                    'year': year,
                    'month': month,
                    'temperature': round(temp, 1),
                    'zone': zone
                })

        return jsonify(historical_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)