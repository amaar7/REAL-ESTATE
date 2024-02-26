import React, { useState, useEffect } from 'react';

function Bookings() {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    fetch('http://localhost:4000/get_all_bookings')
      .then(response => response.json())
      .then(data => setBookings(data.bookings))
      .catch(error => console.error('Error fetching bookings:', error));
  }, []);

  return (
    <div>
      <h2>Bookings</h2>
      <ul>
        {bookings.map(booking => (
          <li key={booking.user_id}>
            User ID: {booking.user_id}, Property ID: {booking.property_id}, Check-in: {booking.check_in_date}, Check-out: {booking.check_out_date}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Bookings;
