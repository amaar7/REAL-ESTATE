import React, { useState, useEffect } from 'react';
import './Properties.css';

function Properties() {
  const [properties, setProperties] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const propertiesPerPage = 12;

  useEffect(() => {
    // Fetch properties from the backend API
    fetch("/get_all_properties")
      .then(response => response.json())
      .then(data => {
        setProperties(data.properties);
      })
      .catch(error => console.error('Error fetching properties:', error));
  }, []);

  // Calculate pagination
  const indexOfLastProperty = currentPage * propertiesPerPage;
  const indexOfFirstProperty = indexOfLastProperty - propertiesPerPage;
  const currentProperties = properties.slice(indexOfFirstProperty, indexOfLastProperty);

  const nextPage = () => {
    if (indexOfLastProperty < properties.length) {
      setCurrentPage(currentPage + 1);
    }
  };

  const prevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  return (
    <div className="properties-container">
      <h2>Properties</h2>
      <div className="pagination">
        <button onClick={prevPage}>Prev</button>
        <button onClick={nextPage}>Next</button>
      </div>
      <div className="property-grid">
        {currentProperties.map(property => (
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
