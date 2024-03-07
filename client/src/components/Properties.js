// Properties.js
import React, { useState, useEffect } from 'react';
import './Properties.css';

function Properties() {
  const [properties, setProperties] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const propertiesPerPage = 12;

  // New state for user details
  const [bookingDetails, setBookingDetails] = useState({
    user_id: 1, // Replace with the actual user ID when implementing user authentication
    property_id: null,
    check_in_date: "",
    check_out_date: "",
  });

  useEffect(() => {
    // Fetch properties from the backend API
    fetch("/get_all_properties")
      .then(response => response.json())
      .then(data => {
        setProperties(data.properties);
      })
      .catch(error => console.error('Error fetching properties:', error));
  }, []);

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

  const handleBookClick = (property) => {
    // Update the property_id in bookingDetails
    setBookingDetails({
      ...bookingDetails,
      property_id: property.id,
    });
  };

  const handleInputChange = (e) => {
    // Update the bookingDetails state based on user input
    setBookingDetails({
      ...bookingDetails,
      [e.target.name]: e.target.value,
    });
  };

  const handleBookingSubmit = (e) => {
    e.preventDefault();

    // Perform the booking creation logic here
    fetch("/create_booking", {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(bookingDetails),
    })
    .then(response => response.json())
    .then(data => {
      console.log('Booking created successfully:', data);
      // Display a "Booked successfully" message
      const successMessage = document.querySelector('.success-message');
      successMessage.classList.add('show');
      // Hide the success message after 3 seconds (3000 milliseconds)
      setTimeout(() => {
        successMessage.classList.remove('show');
      }, 3000);
      // You can add any additional logic or UI updates here
    })
    .catch(error => console.error('Error creating booking:', error));

    // Reset property_id and input fields after submitting
    setBookingDetails({
      ...bookingDetails,
      property_id: null,
      check_in_date: "",
      check_out_date: "",
    });
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
          <div key={property.id} className="property-card">
            <img src={property.image_link} alt={property.title} />
            <div className="property-details">
              <h3>{property.title}</h3>
              <p>{property.location}</p>
              <p>${property.price}</p>
              <button onClick={() => handleBookClick(property)}>Book</button>
            </div>
          </div>
        ))}
      </div>
      {/* Display the booking form if property_id is set */}
      {bookingDetails.property_id && (
        <div className="booking-form">
          <h2>Booking Form</h2>
          <form onSubmit={handleBookingSubmit}>
            <label>
              Check-in Date:
              <input
                type="text"
                name="check_in_date"
                value={bookingDetails.check_in_date}
                onChange={handleInputChange}
                required
              />
            </label>
            <label>
              Check-out Date:
              <input
                type="text"
                name="check_out_date"
                value={bookingDetails.check_out_date}
                onChange={handleInputChange}
                required
              />
            </label>
            <div className="form-buttons">
              <button type="submit">Book</button>
              <button type="button" onClick={() => setBookingDetails({ ...bookingDetails, property_id: null })}>Cancel</button>
            </div>
          </form>
        </div>
      )}
      {/* Success message */}
      <div className="success-message">Booked successfully!</div>
      
    </div>
  );
}

export default Properties;
