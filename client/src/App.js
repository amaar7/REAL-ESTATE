import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Users from './components/Users';
import Properties from './components/Properties';
import Bookings from './components/Bookings';

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <ul>
            <li>
              <Link to="/users">Users</Link>
            </li>
            <li>
              <Link to="/properties">Properties</Link>
            </li>
            <li>
              <Link to="/bookings">Bookings</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/users" element={<Users />} />
          <Route path="/properties" element={<Properties />} />
          <Route path="/bookings" element={<Bookings />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
