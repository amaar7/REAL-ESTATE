import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';


function Home() {
  return (
    <div className="home-container">
      <div className="home-content">
        <h1>Welcome to Dream Homes</h1>
        <p>Your Gateway to Exceptional Living</p>
        <Link to="/properties" className="explore-link">Explore Properties</Link>
      </div>
    </div>
  );
}

export default Home;
