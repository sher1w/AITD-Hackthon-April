import React, { useState } from 'react';
import axios from 'axios';

function FishPredictor() {
  const [salinity, setSalinity] = useState('');
  const [temperature, setTemperature] = useState('');
  const [result, setResult] = useState(null);

  const handlePredict = async () => {
    const salinityValue = parseFloat(salinity);
    const temperatureValue = parseFloat(temperature);

    if (isNaN(salinityValue) || isNaN(temperatureValue)) {
      setResult('Please enter valid numeric values.');
      return;
    }

    try {
      const res = await axios.post('http://localhost:5000/predict', {
        salinity: salinityValue,
        temperature: temperatureValue,
      });
      setResult(res.data.fish_present ? 'Fish likely present 🐟' : 'No fish detected ❌');
    } catch (err) {
      console.error(err);
      setResult('Prediction failed.');
    }
  };

  return (
    <div>
      <h2>🐠 Fish Predictor</h2>
      <input
        type="number"
        placeholder="Salinity"
        value={salinity}
        onChange={(e) => setSalinity(e.target.value)}
      />
      <input
        type="number"
        placeholder="Temperature"
        value={temperature}
        onChange={(e) => setTemperature(e.target.value)}
      />
      <button onClick={handlePredict}>Predict</button>
      {result && <p>{result}</p>}
    </div>
  );
}

export default FishPredictor;
