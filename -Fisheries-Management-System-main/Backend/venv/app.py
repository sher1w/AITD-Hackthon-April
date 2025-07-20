from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/data')
def get_data():
    df = pd.read_csv('goa_ocean_data.csv')  # Use the actual file name
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)
