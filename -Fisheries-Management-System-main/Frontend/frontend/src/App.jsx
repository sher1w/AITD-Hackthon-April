import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './Home';
import FishPredictor from './FishPredictor';
import Navbar from './Navbar';
import FishFinder from './FishFinder';
function App() {
  return (
    <Router>
      <Navbar /> {/* Add Navbar here */}
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/predict" element={<FishPredictor />} />
        <Route path="/finder" element={<FishFinder/>} />
      </Routes>
    </Router>
  );
}

export default App;
