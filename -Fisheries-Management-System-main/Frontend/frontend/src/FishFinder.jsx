import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
} from 'chart.js';
import './FishFinder.css';

ChartJS.register(ArcElement, Tooltip, Legend);

function FishFinder() {
  const [temperature, setTemperature] = useState(28);
  const [month, setMonth] = useState(5);
  const [result, setResult] = useState(null);
  const [currentTemp, setCurrentTemp] = useState(null);
  const [historicalData, setHistoricalData] = useState([]);
  const [loading, setLoading] = useState(false);

  // Fetch current temperature and historical data on mount
  useEffect(() => {
    const fetchTemperature = async () => {
      try {
        const response = await axios.get('http://localhost:5000/get_temperature');
        setCurrentTemp(response.data.temperature);
      } catch (error) {
        console.error('Error fetching temperature:', error);
        
      }
    };
    fetchTemperature();

    const fetchHistoricalData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/historical_migration');
        setHistoricalData(response.data);
      } catch (error) {
        console.error('Error fetching historical data:', error);
        setHistoricalData([]);
      }
    };
    fetchHistoricalData();
  }, []);

  const predictMigration = async () => {
    setLoading(true);
    setResult(null);
    try {
      console.log('Sending:', { temperature, month });
      const response = await axios.post('http://localhost:5000/find_fish', {
        temperature,
        month
      }, {
        headers: { 'Content-Type': 'application/json' }
      });
      console.log('Received:', response.data);
      setResult(response.data);
      document.title = `Goa Fish Finder - ${response.data.zone}`;
    } catch (error) {
      console.error('Error:', error);
      setResult({ zone: 'Error', tip: `Failed to predict migration. ${error.message}` });
      document.title = 'Goa Fish Finder - Error';
    }
    setLoading(false);
  };

  // Prepare data for pie chart
  const prepareChartData = () => {
    const zoneCounts = {
      Calangute: historicalData.filter(d => d.zone === 'Calangute').length,
      Baga: historicalData.filter(d => d.zone === 'Baga').length,
      Colva: historicalData.filter(d => d.zone === 'Colva').length,
    };

    return {
      labels: ['Calangute', 'Baga', 'Colva'],
      datasets: [
        {
          data: [zoneCounts.Calangute, zoneCounts.Baga, zoneCounts.Colva],
          backgroundColor: [
            'rgba(46, 139, 87, 0.6)',  // Calangute (green)
            'rgba(255, 165, 0, 0.6)',  // Baga (orange)
            'rgba(255, 99, 132, 0.6)', // Colva (pink)
          ],
          borderColor: [
            'rgba(46, 139, 87, 1)',
            'rgba(255, 165, 0, 1)',
            'rgba(255, 99, 132, 1)',
          ],
          borderWidth: 1,
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'Migration Zone Distribution',
      },
    },
  };

  const chartData = prepareChartData();

  return (
    <div className="app">
      <header>
        <h1>Goa Fish Hotspot Finder</h1>
        <p>Find sustainable fishing zones</p>
      </header>
      <main>
        <div className="input-group">
          <label htmlFor="temperature">Sea Temperature (°C)</label>
          <input
            type="range"
            id="temperature"
            min="26"
            max="32"
            value={temperature}
            onChange={(e) => setTemperature(Number(e.target.value))}
          />
          <span>{temperature}°C )</span>
        </div>
        <div className="input-group">
          <label htmlFor="month">Month</label>
          <select
            id="month"
            value={month}
            onChange={(e) => setMonth(Number(e.target.value))}
          >
            <option value="1">January</option>
            <option value="2">February</option>
            <option value="3">March</option>
            <option value="4">April</option>
            <option value="5">May</option>
            <option value="6">June</option>
            <option value="7">July</option>
            <option value="8">August</option>
            <option value="9">September</option>
            <option value="10">October</option>
            <option value="11">November</option>
            <option value="12">December</option>
          </select>
        </div>
        <button onClick={predictMigration} disabled={loading}>
          {loading ? 'Finding Hotspot...' : 'Find Hotspot'}
        </button>
        {result && (
          <div className="result">
            <h3>
              Fish near {result.zone}!{' '}
              <span className={`health-indicator ${result.color || 'red'}`}></span>
            </h3>
            <p>SST: {result.sst || 'N/A'}°C, Chlorophyll: {result.chlorophyll || 'N/A'} mg/m³, Current: {result.current || 'N/A'} m/s</p>
            <p className="tip">Tip: {result.tip}</p>
            <p>Sustainability Score: {result.score || 'N/A'}/100</p>
          </div>
        )}
        <div className="historical">
          <h3>Historical Migration Patterns</h3>
          <table>
            <thead>
              <tr>
                <th>Year</th>
                <th>Month</th>
                <th>Temperature (°C)</th>
                <th>Zone</th>
              </tr>
            </thead>
            <tbody>
              {historicalData.map((data, index) => (
                <tr key={index}>
                  <td>{data.year}</td>
                  <td>{data.month}</td>
                  <td>{data.temperature}</td>
                  <td>{data.zone}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="chart-container">
          <h3>Pie Chart: Migration Zone Distribution</h3>
          <Pie data={chartData} options={chartOptions} />
        </div>
      </main>
      <footer>
        <p>Helping Goa’s fishermen thrive sustainably</p>
      </footer>
    </div>
  );
}

export default FishFinder;