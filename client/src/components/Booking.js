// Booking.js
import React, { useState, useEffect } from 'react';
import './Booking.css';

function Booking() {
  const [bookedProperties, setBookedProperties] = useState([]);

  useEffect(() => {
    fetch("/get_all_bookings")
      .then(response => response.json())
      .then(data => {
        setBookedProperties(data.bookings || []); // Ensure it's initialized as an array
      })
      .catch(error => console.error('Error fetching bookings:', error));
  }, []);

  return (
    <div className="booking-container">
      <h2>Booking</h2>
      <div className="booked-properties">
        {bookedProperties.map(booking => (
          <div key={booking.id} className="booked-property-card">
            <img src={booking.property_image_link} alt={`Booked Property ${booking.id}`} />
            <div className="booked-property-details">
              <h3>Property ID: {booking.property_id}</h3>
              <p>User ID: {booking.user_id}</p>
              <p>Check-in: {booking.check_in_date}</p>
              <p>Check-out: {booking.check_out_date}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Booking;
