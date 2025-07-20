// Navbar.jsx
import React from 'react';
import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={{ padding: '10px', backgroundColor: '#333', color: '#fff' }}>
      <ul style={{ listStyleType: 'none', display: 'flex', gap: '20px' }}>
        <li>
          <Link to="/" style={{ color: '#fff', textDecoration: 'none' }}>
            Home
          </Link>
        </li>
      
        <li>
          <Link to="/predict" style={{ color: '#fff', textDecoration: 'none' }}>
            Fish Predictor
          </Link>
        </li>  <li>
          <Link to="/finder" style={{ color: '#fff', textDecoration: 'none' }}>
            Fish Predictor
          </Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
