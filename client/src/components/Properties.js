import React, { useState, useEffect } from 'react';

function Properties() {
  const [properties, setProperties] = useState([]);

  useEffect(() => {
    fetch('http://localhost:4000/get_all_properties')
      .then(response => response.json())
      .then(data => setProperties(data.properties))
      .catch(error => console.error('Error fetching properties:', error));
  }, []);

  return (
    <div>
      <h2>Properties</h2>
      <ul>
        {properties.map(property => (
          <li key={property.title}>{property.title} - {property.price} - {property.location}</li>
        ))}
      </ul>
    </div>
  );
}

export default Properties;
