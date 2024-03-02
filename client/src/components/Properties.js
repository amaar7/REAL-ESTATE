import React, { useState, useEffect } from 'react';
import './Properties.css';

function Properties() {
  const [properties, setProperties] = useState([]);

  useEffect(() => {
    // Fetch properties from the backend API
    fetch("/get_all_properties")
      .then(response => response.json())
      .then(data => {
        setProperties(data.properties);
      })
      .catch(error => console.error('Error fetching properties:', error));
  }, []);

  return (
    <div className="properties-container">
      <h2>Properties</h2>
      <div className="property-grid">
        {properties.map(property => (
          <div key={property.title} className="property-card">
            <img src={property.image_link} alt={property.title} />
            <div className="property-details">
              <h3>{property.title}</h3>
              <p>{property.location}</p>
              <p>${property.price}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Properties;
