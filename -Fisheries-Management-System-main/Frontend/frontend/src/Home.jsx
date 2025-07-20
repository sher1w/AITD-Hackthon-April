import React from 'react';
import { Link } from 'react-router-dom';

function Home() {
  return (
    <div>
      <h1>Welcome to the Fish Predictor App</h1>
      <Link to="/predict">Go to Fish Predictor</Link>
      <Link to="/find">Go to Fish Predictor</Link>
    </div>
  );
}

export default Home;
