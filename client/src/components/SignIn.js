// src/components/SignIn.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate from react-router-dom
import './SignIn.css';

function SignIn() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const navigate = useNavigate(); // Get the navigate function from React Router

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSignIn = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:4000/user_signin', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      console.log(data); // Log the response from the server

      // Check if sign-in was successful before redirecting
      if (response.ok) {
        // Redirect to the Properties page
        navigate('/properties');
      } else {
        // Handle sign-in error (e.g., display error message)
      }

    } catch (error) {
      console.error('Error signing in:', error);
      // Handle other errors (e.g., display error message)
    }
  };

  return (
    <div className="signup-container">
      <h2>Sign In</h2>
      <form onSubmit={handleSignIn}>
        <label htmlFor="username">Username:</label>
        <input
          type="text"
          id="username"
          name="username"
          value={formData.username}
          onChange={handleChange}
          required
        />

        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          required
        />

        <button type="submit">Sign In</button>
      </form>
    </div>
  );
}

export default SignIn;
